# Script to compose OPDS feed from output of oapen_extract_data.

from lxml import etree
from lxml.builder import ElementMaker
import dcps_utils as util
from pprint import pprint
from datetime import datetime


contentProvider = "OAPEN"

NSMAP = {None: "http://www.w3.org/2005/Atom",
         'app': "http://www.w3.org/2007/app",
         'bibframe': "http://bibframe.org/vocab/",
         'dcterms': "http://purl.org/dc/terms/",
         'simplified': "http://librarysimplified.org/terms/",
         'opds': "http://opds-spec.org/2010/catalog",
         'schema': "http://schema.org/"}


def main():

    now = datetime.today().isoformat()  # Current timestamp in ISO
    base_url = "https://ebooks.library.columbia.edu/static-feeds/oapen/"
    base_folder = 'output/oapen/'

    pickle_barrel = ['oapen_extract_1.pickle',
                     'oapen_extract_2.pickle',
                     'oapen_extract_3.pickle',
                     'oapen_extract_4.pickle',
                     'oapen_extract_5.pickle',
                     'oapen_extract_6.pickle',
                     'oapen_extract_7.pickle',
                     'oapen_extract_8.pickle',
                     'oapen_extract_9.pickle',
                     'oapen_extract_10.pickle',
                     ]

    feed_stem = 'oapen_clio'

    for a_feed in pickle_barrel:
        idx = int(a_feed.split('.')[0].split('_')[-1])
        # print(idx)
        in_file = base_folder + a_feed

        if idx > 1:
            feed_name = feed_stem + '_p' + str(idx) + '.xml'
        else:
            feed_name = feed_stem + '.xml'
        feed_next = feed_stem + '_p' + str(idx + 1) + '.xml'

        root = etree.Element("feed", nsmap=NSMAP)
        feed_id = etree.SubElement(root, "id")
        feed_id.text = base_url + "oapen_clio"
        feed_title = etree.SubElement(root, "title")
        feed_title.text = "OAPEN Book Collection | Columbia University Libraries"
        feed_updated = etree.SubElement(root, "updated")
        feed_updated.text = now
        feed_link = etree.SubElement(
            root, "link", href=base_url + feed_name, rel="self")
        feed_link_next = etree.SubElement(
            root, "link", href=base_url + feed_next, rel="next", title="Next")

        # the_data = util.unpickle_it('output/oapen_ERC_data.pickle')
        the_data = util.unpickle_it(in_file)

        for record in the_data:

            make_entry(root, record)

            # with open('output/oapen_clio/oapen_clio_' + str(now) + '.xml', 'wb') as f:
            with open(base_folder + feed_name, 'wb') as f:
                f.write(etree.tostring(root, pretty_print=True))


def make_entry(_parent, _dict):
    ns_bibframe = "{%s}" % NSMAP["bibframe"]
    ns_dcterms = "{%s}" % NSMAP["dcterms"]
    ns_simplified = "{%s}" % NSMAP["simplified"]

    # process bitstreams (binary file links)
    e_bitstreams = process_bitstreams(_dict['bitstreams'])
    # e_metadata = process_metadata(_dict['metadata'])
    e_metadata = _dict['metadata']

    if e_bitstreams and 'link_pdf' in e_bitstreams:
        # if there is no bitstream data, we can't use the entry.
        # TODO: test if either PDF or EPUB.

        # Create <entry> element
        entry = etree.SubElement(_parent, "entry")

        # Add elements within entry
        e_id = etree.SubElement(entry, "id")
        # e_id.text = e_metadata['id']
        e_id.text = metadata_finder(e_metadata, 'dc.identifier.uri')[0]

        # search for authors
        author_data = metadata_finder(e_metadata, 'dc.contributor.author')
        print(author_data)
        # e_metadata['authors'] = [{'a_name': a} for a in author_data]

        # for aut in e_metadata['authors']:
        for aut in author_data:
            e_author = etree.SubElement(entry, "author")
            e_author_name = etree.SubElement(e_author, "name")
            e_author_name.text = aut
            e_author_name_sort = etree.SubElement(
                e_author, ns_simplified + "sort_name")
            e_author_name_sort.text = aut

        e_title = etree.SubElement(entry, "title")
        print(_dict['name'])
        e_title.text = _dict['name']
        e_dist = etree.SubElement(
            entry, ns_bibframe + "distribution",  ProviderName=contentProvider)
        e_link_pdf = etree.SubElement(
            entry, "link", href=e_bitstreams['link_pdf'], type="application/pdf", rel="http://opds-spec.org/acquisition/open-access")
        if 'link_cover' in e_bitstreams:
            print(e_bitstreams['link_cover'])
            e_link_cover = etree.SubElement(
                entry, "link", href=e_bitstreams['link_cover'], type="image/jpeg", rel="http://opds-spec.org/image")
            e_link_cover = etree.SubElement(
                entry, "link", href=e_bitstreams['link_cover'], type="image/jpeg", rel="http://opds-spec.org/image/thumbnail")

        # e_summary = etree.SubElement(entry, "summary", type="text")
        # e_updated = etree.SubElement(entry, "updated")
        # e_issued = etree.SubElement(entry, ns_dcterms + "issued")
        # e_published = etree.SubElement(entry, "published")

        # pub dates
        pub_issued = metadata_finder(e_metadata, 'dc.date.issued')
        if pub_issued:
            e_issued = etree.SubElement(entry, ns_dcterms + "issued")
            e_issued.text = pub_issued[0]

        # Published should be same as issued? Not sure if .available is correct.
        pub_published = metadata_finder(e_metadata, 'dc.date.available')
        if pub_published:
            e_published = etree.SubElement(entry, "published")
            e_published.text = pub_published[0]

        # # updated
        e_updated = etree.SubElement(entry, "updated")
        e_updated.text = convert_date(_dict['lastModified'])

        # updated = metadata_finder(e_metadata, "dc.date.available")
        # if updated:
        #     e_updated = etree.SubElement(entry, "updated")
        #     e_updated.text = updated[0]

        # Language
        languages = metadata_finder(
            e_metadata, 'dc.language', result_key='code')
        if languages:
            for l in languages:
                e_language = etree.SubElement(entry, ns_dcterms + "language")
                e_language.text = l

        # # Summary
        # summary = metadata_finder(e_metadata, 'dc.description.abstract')
        # if summary:
        #     e_summary = etree.SubElement(entry, "summary", type="text")
        #     e_summary.text = summary[0]

        # Content
        content = metadata_finder(e_metadata, 'dc.description.abstract')
        e_content = etree.SubElement(entry, "content", type="text/html")
        if content:
            e_content_p1 = etree.SubElement(e_content, "p")
            e_content_p1.text = content[0]
        e_content_p2 = etree.SubElement(e_content, "p")
        e_content_clio_link = etree.SubElement(
            e_content_p2, "a", href='https://clio.columbia.edu/catalog/' + str(_dict['' 'cul_bibid']))
        e_content_clio_link.text = "View catalog record in CLIO."

        # publisher
        publisher = metadata_finder(e_metadata, 'publisher.name')
        if publisher:
            e_summary = etree.SubElement(entry, ns_dcterms + "publisher")
            e_summary.text = publisher[0]

        # Audience
        e_audience = etree.SubElement(
            entry, "category", term="Adult", label="Adult", scheme="http://schema.org/audience")

        # Nonfiction
        # TODO: check that this applies to all
        e_fiction_category = etree.SubElement(entry, "category", term="http://librarysimplified.org/terms/fiction/Nonfiction",
                                              label="Nonfiction", scheme="http://librarysimplified.org/terms/fiction/")

        # Subjects
        subjs = metadata_finder(e_metadata, 'dc.subject.other')
        if subjs:
            for s in subjs:
                e_subj = etree.SubElement(
                    entry, "category", term=s, label=s, scheme="http://www.bic.org.uk/7/BIC-Standard-Subject-Categories/")


def metadata_finder(_list, _keyValue, result_key='value'):
    return [m[result_key]
            for m in _list if result_key in m and m['key'] == _keyValue]


def process_bitstreams(_list):

    url = 'http://library.oapen.org'

    result = {}
    if len(_list) > 0:
        for b in _list:
            if b['mimeType'] == "application/pdf":
                result['link_pdf'] = url + b["retrieveLink"]
            elif b['mimeType'] == "image/jpeg":
                result['link_cover'] = url + b["retrieveLink"]
            elif b['mimeType'] == "text/plain":
                result['link_text'] = url + b["retrieveLink"]

    return result


def convert_date(_datetime):
    # Convert date of format "2020-04-02 12:32:17.628" to ISO
    d = datetime.strptime(_datetime, '%Y-%m-%d %H:%M:%S.%f')
    return d.isoformat()


if __name__ == "__main__":
    main()
