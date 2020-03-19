


icons = {'facesmiling':'\U0001F600',
        'redx':'\U0000274C',  # use for parse errors
        'exclamation':'\U00002757',
        'warning':'\U000026A0\U0000FE0F',  # use for schema validation errors
        'qmark':'\U00002753'}

print(icons['warning'])

quit()


a_file = '/some/path/to/as_ead_ldpd_12028538.xml'

file_name = a_file.split('/')[-1]
bibid = file_name.split('_')[-1].split('.')[0]

print(bibid)