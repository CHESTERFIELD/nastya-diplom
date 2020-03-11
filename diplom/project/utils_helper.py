import os
import re
import inspect
from collections import OrderedDict

import datetime

from django.db import connections
from django.utils.encoding import smart_str
import time


def prn(value, level=0, is_log=0):
    # if not DEBUG:
    #     return False

    max_level_show = 1

    def is_last_level(value):
        if isinstance(value, (float, int, str)):
            return 1
        return 0

    def print_like_string(value):
        output = ''
        if isinstance(value, (float, int, str, bool,)):
            output = "%s(%s)" % (value, type(value))
        if isinstance(value, (list, dict, set, tuple)):
            output = "%s(%s)" % (value, type(value))

        if isinstance(value, (datetime.time, datetime.date)):
            output = "%s(%s)" % (value, type(value))

        if not output:
            try:
                output = "%s(%s)" % (str(value), type(value))
            except TypeError:
                prn(value)
        #print(type(value))
        return output

    if level == 0:
        print('')
        frame = inspect.currentframe()
        try:
            context = inspect.getframeinfo(frame.f_back).code_context
            try:
                caller_lines = ''.join([line.strip() for line in context])
            except TypeError:
                caller_lines = str(context)
            m = re.search(r'echo\s*\((.+?)\)$', caller_lines)
            if m:
                caller_lines = m.group(1)
            output = "********************   "+caller_lines.replace('prn(', '')[:-1]+"  ***********************"
            print(output)
            print(type(value))
        finally:
            del frame
    level_str = '   '
    cur_level = level
    while level != 0:
        level_str += '   '
        level -= 1

    if isinstance(value, (list, set, tuple)):
        if not value:
            print(print_like_string(value))
        for key, sub_value in enumerate(value):
            output = level_str+'['+str(key)+'] = ' + print_like_string(sub_value)
            print(output)
            if cur_level < max_level_show and not is_last_level(sub_value):
                prn(sub_value, cur_level+1, is_log)
    elif isinstance(value, (dict, OrderedDict)):
        if not value:
            print(print_like_string(value))
        for key, sub_value in value.items():
            output = level_str+'['+smart_str(key)+'] = ' + print_like_string(sub_value)
            print(output)

            if cur_level < max_level_show and not is_last_level(sub_value):
                prn(sub_value, cur_level+1, is_log)
    else:
        # string_print = print_like_string(value)
        # if string_print:
        value_type = get_type(value)
        if value_type == 'model':
            # print django model
            clean_fields = {}
            for key, item in value.__dict__.items():
                if not key.startswith('_'):
                    clean_fields[key] = item
            prn(clean_fields, cur_level+1, is_log)
        elif value_type == 'date':
            print("%s(%s)" % (value, type(value)))
        elif value_type == 'queryset':
            # print django queryset
            for one_record in value:
                print('')
                print(print_like_string(one_record))
                prn(one_record, cur_level + 1, is_log)
            print('Count records in queryset: %s' % value.count())
        else:
            if isinstance(value_type, (str)):
                print(print_like_string(value))
            else:
                #
                if '<class' in str(value_type):
                    if hasattr(value, '__dict__'):
                        prn(value.__dict__, cur_level + 1, is_log)
                    else:
                        print(print_like_string(value))
                    # for attr_name in dir(value):
                    #     try:
                    #         attr_value = getattr(value, attr_name)
                    #     except AttributeError:
                    #         pass
                    #     if get_type(attr_value) not in ['function_or_method', 'method']:
                    #         output = level_str + '[' + str(attr_name) + '] = ' + print_like_string(attr_value)
                    #         print(output)
                else:
                    print(print_like_string(value))

    if cur_level == 0:
        output = '**********************************************************************'
        print(output)
        print(' ')
    return True


def get_type(value):
    type_result = ''
    if isinstance(value, bool):
        return 'bool'
    if isinstance(value, (float, int, str, list, dict, set, tuple)):
        return str(type(value))
    value_type_str = str(type(value))
    if '<class' in value_type_str and '.models.' in value_type_str:
        type_result = 'model'
    if 'builtin_function_or_method' in value_type_str:
        type_result = 'builtin_function_or_method'
    if "<class 'method'" in value_type_str:
        type_result = 'method'
    if "<class 'datetime.date'>" in value_type_str:
        type_result = 'date'
    if "<class 'django.db.models.query.QuerySet'>" in value_type_str:
        type_result = 'queryset'
    if "<class 'django.contrib.gis.geos.point.Point'>" in value_type_str:
        type_result = 'geo_point'

    if not type_result:
        print('type str = "%s"' % value_type_str)
        type_result = type(value)
    return type_result


def print_queries(start_number=0, end_number=False, count_last=False, is_scrapy_log=False, summary=False):
    count_total = len(connections['default'].queries)
    duplicates = {}
    count_duplicates = 0
    db_time = 0
    for number, item in enumerate(connections['default'].queries):
        need_print = False
        if not start_number or number >= start_number:
            if not end_number or number <= end_number:
                if not count_last or number >= count_total - count_last:
                    need_print = True
        if need_print:
            # str1 = ' '
            # str2 = "**********   %s QUERY,  TIME: %s, **************   " % (number, item['time'])
            # str3 = smart_str(item['sql'])
            # if is_scrapy_log:
            #     from scrapy import log
            #     log.msg(str1)
            #     log.msg(str2)
            #     log.msg(str3)
            # else:
            db_time += float(item['time'])
            sql_string = smart_str(item['sql'])
            if not summary:
                print_one_sql(item, number)

            if sql_string not in duplicates:
                duplicates[sql_string] = {'count_dupl': 1,
                                          'item': item,
                                          'number': number + 1}
            else:
                duplicates[sql_string]['count_dupl'] += 1
                count_duplicates += 1

    if count_duplicates:
        for sql, sql_info in duplicates.items():
            if sql_info['count_dupl'] > 1:
                print_one_sql(sql_info['item'], sql_info['number'], sql_info['count_dupl'])
    print("")
    print("************************* TOTAL INFO ******************************")
    print("Total queries: %s, Duplicates: %s, Queries time: %s" %
          (count_total, count_duplicates, round(db_time, 6)))


def print_one_sql(item, number, count_duplicates=0):
    sql_string = smart_str(item['sql'])
    print(' ')
    title = "**********   %s QUERY,  TIME: %s, **************   "
    if count_duplicates:
        title = "**********   DUPLICATE QUERY %s, TIME: %s, COUNT OF DUPLICATES " \
                + str(count_duplicates) + " **************   "

    print(title % (number + 1, item['time']))
    print(sql_string)


def parametrized(dec):
    def layer(*args, **kwargs):
        def repl(f):
            return dec(f, *args, **kwargs)
        return repl
    return layer


# @parametrized
def analyze(method):
    # example to use: before function add line
    # @analyze()
    # def func_name():
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        #print 'Function %r (%r, %r) =  %2.2f sec' % \
        #      (method.__name__, args, kw, te-ts)
        time_string = humanize_seconds(round(te - ts, 2))
        # minutes = 0
        # hours = 0
        # if seconds > 60:
        #     minutes = seconds // 60
        #     seconds = seconds - minutes * 60
        # if minutes > 60:
        #     hours = minutes // 60
        #     minutes = minutes - hours * 60
        # time_string = '%ssec.' % seconds
        # if minutes:
        #     time_string = '%sm. %ssec.' % (int(minutes), int(seconds))
        # if hours:
        #     time_string = '%sh. %smin. %ssec' % (int(hours), int(minutes), int(seconds))

        print_queries(summary=False)

        print('Function %r, execution time = %s' % \
              (method.__name__, time_string))
        print("*******************************************************************")
        return result

    return timed


def humanize_seconds(seconds):
    """Show seconds in human form, e.g. 60 is "1 minute", 7200 is "2
    hours".

    :keyword prefix: Can be used to add a preposition to the output,
        e.g. 'in' will give 'in 1 second', but add nothing to 'now'.

    """
    minutes = 0
    hours = 0
    days = 0
    if seconds > 60:
        minutes = seconds // 60
        seconds = seconds - minutes * 60
    if minutes > 60:
        hours = minutes // 60
        minutes = minutes - hours * 60
    if hours > 24:
        days = hours // 24
        hours = hours - days * 24
    time_string = '%ssec.' % seconds

    hours_text = declension(hours, 'hour', 'hours')
    days_text = declension(days, 'day', 'days')
    if minutes:
        time_string = '{0} min. {1} sec.'.format(int(minutes), int(seconds))
    if hours:
        time_string = '{0} {1} {2} min.'.format(int(hours), hours_text, int(minutes))
    if days:
        time_string = '{0} {1} {2} {3}'.format(int(days), days_text, int(hours), hours_text)

    return time_string


def declension(count, variant_1, variant_2):
    # variant_1 - example 1-year, 1-day
    # variant_2 - example 3-years, 3-days
    if count != 0:
        # if count > 100:
        #     num = int(str(count)[-2:])
        # else:
        #     num = count

        # num = int(str(num)[-1:])
        if count == 1:
            result = variant_1
        else:
            result = variant_2
        return result
    else:
        return variant_2


def translit_ru_to_en(text):
    "Russian translit: converts 'привет'->'privet'"

    table = {u'а': 'a', u'б': 'b', u'в': 'v', u'г': 'g', u'д': 'd', u'е': 'e', u'ё': 'e', u'з': 'z',
             u'и': 'i', u'й': 'j', u'к': 'k', u'л': 'l', u'м': 'm', u'н': 'n', u'о': 'o', u'п': 'p',
             u'р': 'r', u'с': 's', u'т': 't', u'у': 'u', u'ф': 'f', u'х': 'h', u'ъ': "'", u'ы': 'y',
             u'ь': "'", u'э': 'e', u'А': 'A', u'Б': 'B', u'В': 'V', u'Г': 'G', u'Д': 'D', u'Е': 'E',
             u'Ё': 'E', u'З': 'Z', u'И': 'I', u'Й': 'J', u'К': 'K', u'Л': 'L', u'М': 'M', u'Н': 'N',
             u'О': 'O', u'П': 'P', u'Р': 'R', u'С': 'S', u'Т': 'T', u'У': 'U', u'Ф': 'F', u'Х': 'H',
             u'Ъ': "'", u'Ы': 'Y', u'Ь': "'", u'Э': 'E', u'ж': 'zh', u'ц': 'ts', u'ч': 'ch', u'ш': 'sh',
             u'Ш': 'SH', u'Щ': 'SCH', u'щ': 'sch', u'ю': 'ju', u'я': 'ja',  u'Ю': 'JU', u'Я': 'JA',
             u'Ж': 'Zh', u'Ц': 'Ts', u'Ч': 'Ch'}

    translit = u''
    for i, item in enumerate(text):
        if item in table:
            item = table[item]
        translit += item
    return translit


def check_path_dirs(directory):
    directory_segments = directory.split('/')
    clean_directory = "/".join(directory_segments[:-1])
    last_folder = directory_segments[len(directory_segments)-1]
    if '.' not in last_folder:
        clean_directory += last_folder

    if not os.path.exists(clean_directory):
        os.makedirs(clean_directory)

    return True


### START SORT BY ATTR ####

def sort_by_attr(sort_object, key_name, direction=1):
    sort_list = []
    if type(sort_object) == dict:
        for key, item in sort_object.items():
            sort_list.append(item)
    else:
        if type(sort_object) == list:
            sort_list = sort_object
        else:
            for key, item in enumerate(sort_object):
                sort_list.append(item)

    sort_dict = sorted(sort_list, key=lambda k: sort_key(k, key_name, direction))

    return sort_dict


def sort_key(k, key_name, direction):
    if type(k) == dict:
        return k[key_name]*direction
    else:
        return getattr(k, key_name)*direction

### STOP SORT BY ATTR ####


def truncate_float(value, digits_after_point=2):
    pow_10 = 10 ** digits_after_point
    return (float(int(value * pow_10))) / pow_10


def check_same_items(a, b):
    return (set(a) & set(b))
