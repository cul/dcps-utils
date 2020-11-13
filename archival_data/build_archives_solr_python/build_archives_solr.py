# build.py
import sys
import os
import acfa
import archival_collections_extract
import ohac_extract


def main():
    solr_index_envs = []
    if len(sys.argv) > 1:
        solr_index_envs = sys.argv[1].split(',')
    else:
        # Exit because there was no argument dev|test|prod.
        sys.exit("Error: No solr_index_env argument(s) provided!")
    solr_update_urls = ["http://ldpd-solr-" + solr_index_env +
                        "1.cul.columbia.edu:8983/solr/archives_portal/update" for solr_index_env in solr_index_envs]
    for solr_xml_path in archival_collections_extract.main():
        for solr_update_url in solr_update_urls:
            acfa.run_post(solr_xml_path, solr_update_url)
    for solr_xml_path in ohac_extract.main():
        for solr_update_url in solr_update_urls:
            acfa.run_post(solr_xml_path, solr_update_url)
    my_path = os.path.dirname(__file__)
    commit_xml_path = os.path.join(my_path, 'commit.xml')
    delete_xml_path = os.path.join(my_path, 'delete-delta.xml')
    for solr_update_url in solr_update_urls:
        # commit the document add/updates
        acfa.run_post(commit_xml_path, solr_update_url)
        # delete everything that wasn't added/updated in this job
        acfa.run_post(delete_xml_path, solr_update_url)
        # commit the deletes
        acfa.run_post(commit_xml_path, solr_update_url)


if __name__ == '__main__':
    main()
