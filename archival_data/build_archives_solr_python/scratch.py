import sys
import os
import acfa
sys.path.insert(1, '../../archivesspace/as_reports')
import digester

def main():

    my_name = __file__
    script_name = os.path.basename(my_name)



    saxon_path = '../../resources/saxon-9.8.0.12-he.jar'
    in_path = '~/ohac_marc.xml'
    xsl_path = './oral2solr.xsl'
    out_path = '~/ohac_marc_OUT.xml'

    digester.post_digest(script_name, "THIS IS A TEST")

    print(acfa.run_saxon(saxon_path, in_path, xsl_path, out_path))


if __name__ == '__main__':
    main()
