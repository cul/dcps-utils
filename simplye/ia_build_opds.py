# Script to gather ids and bibids for AI assets linked from CLIO, harvest metadata from IA, and compose an OPDS feed for use in SimplyE.

# internet archive python library docs:
# https://archive.org/services/docs/api/internetarchive/

from internetarchive import get_item
from lxml import etree, html
from lxml.builder import ElementMaker
import dcps_utils as util
from pprint import pprint
from datetime import datetime
from sheetFeeder import dataSheet


contentProvider = "CUL: Internet Archive"

# Namespaces to be used in feed.
NSMAP = {None: "http://www.w3.org/2005/Atom",
         'app': "http://www.w3.org/2007/app",
         'bibframe': "http://bibframe.org/vocab/",
         'dcterms': "http://purl.org/dc/terms/",
         'simplified': "http://librarysimplified.org/terms/",
         'opds': "http://opds-spec.org/2010/catalog",
         'schema': "http://schema.org/"}


def divide_list(lst, n):
    # generate n-sized chunks from list.
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def main():

    # x = get_item('liberiadescribed00mill').metadata
    # print(type(x['subject']))
    # quit()

    # feed_stem = 'ia_mwm_feed'
    # collection_title = "Muslim World Manuscripts"
    feed_stem = 'ia_mrp_feed'
    collection_title = "Missionary Research Pamphlets"

    chunk_size = 500

    the_in_sheet = dataSheet(
        '1yTDyd5GQFEsVBiKOnt5T1ejBdXhxhmXVUn6jQ-dg_5I', 'Missionary!A:Z')
    the_out_sheet = dataSheet(
        '1yTDyd5GQFEsVBiKOnt5T1ejBdXhxhmXVUn6jQ-dg_5I', 'errors!A:Z')

    # Initialize the output sheet
    the_out_sheet.clear()
    the_out_sheet.appendData([['collection', 'file', 'bibid', 'id', 'errors']])

    global now
    now = datetime.today().isoformat()  # Current timestamp in ISO
    base_url = "https://ebooks-test.library.columbia.edu"
    base_folder = 'output/output_ia/'

    # get a list of bibids and ia ids to process
    the_inputs = the_in_sheet.getData()
    the_inputs.pop(0)
    the_records = [{'bibid': r[0], 'id':r[6]} for r in the_inputs]

    # Divide list into chunks
    the_chunks = divide_list(the_records, chunk_size)

    for idx, record_chunk in enumerate(the_chunks):

        report_data = []

        page_no = idx + 1
        if page_no > 1:
            feed_name = feed_stem + '_p' + str(page_no) + '.xml'
        else:
            feed_name = feed_stem + '.xml'

        feed_next_name = feed_stem + '_p' + str(page_no + 1) + '.xml'

        # Set up root and top-level elements
        root = etree.Element("feed", nsmap=NSMAP)
        feed_id = etree.SubElement(root, "id")
        feed_id.text = base_url + "/static-feeds/ia_clio"
        feed_title = etree.SubElement(root, "title")
        feed_title.text = collection_title + " | Columbia University Libraries"
        feed_updated = etree.SubElement(root, "updated")
        feed_updated.text = now

        feed_link = etree.SubElement(
            root, "link", href=base_url + "/static-feeds/" + feed_name, rel="self")

        # TODO: omit feed_next if it is the last one
        feed_link_next = etree.SubElement(
            root, "link", href=base_url + "/static-feeds/" + feed_next_name, rel="next", title="Next")

        for record in record_chunk:

            print(record)
            record_metadata = get_item(record['id']).metadata
            # pprint(record_metadata)

            e = make_entry(root, record_metadata, record['bibid'])
            if e:  # if there are errors emanating from entry, add them to dict.
                record['errors'] = e
            else:
                record['errors'] = ''

            report_data.append(record)

        # Save result xml tree
        with open(base_folder + feed_name, 'wb') as f:
            f.write(etree.tostring(root, pretty_print=True))

        # report results to google sheet
        results = [[collection_title, feed_name, d['bibid'], d['id'], '; '.join(
            d['errors'])] for d in report_data]

    # the_out_sheet.clear()
        the_out_sheet.appendData(results)

    # fin


def make_entry(_parent, _dict, _bibid):
    # collect errors to return for reporting
    global errors
    errors = []

    if not(_dict):
        # If IA returns no data
        print("No data! Skipping...")
        errors.append('Error: No data!')
        return errors

    ia_base_url = 'https://archive.org/download/'
    # define namespaces
    ns_bibframe = "{%s}" % NSMAP["bibframe"]
    ns_dcterms = "{%s}" % NSMAP["dcterms"]
    ns_simplified = "{%s}" % NSMAP["simplified"]

    # Create <entry> element
    entry = etree.SubElement(_parent, "entry")

    # Add subelements using functions
    add_subelement(entry, "id", "identifier", _dict,
                   formated="urn:x-internet-archive:ebooks-app:item:%s")
    add_subelement(entry, "title", "title", _dict)
    add_subelement_static(entry, "distribution",
                          nspace=ns_bibframe, ProviderName=contentProvider)

    # Authors/creators
    if 'creator' in _dict:
        the_creators = _dict['creator']
        if type(the_creators) == list:
            for c in the_creators:
                e_author = etree.SubElement(entry, "author")
                add_subelement_static(e_author, "name", c)
                add_subelement_static(e_author, "sort_name",
                                      c, nspace=ns_simplified)
        else:
            c = the_creators
            e_author = etree.SubElement(entry, "author")
            add_subelement_static(e_author, "name", c)
            add_subelement_static(e_author, "sort_name",
                                  c, nspace=ns_simplified)
    else:
        print('Warning: No *creator* key value!')
        errors.append('creator')

    # Links to resources
    add_subelement_static(entry, "link", href=ia_base_url + str(_dict['identifier']) + "/" + str(
        _dict['identifier']) + ".pdf", type="application/pdf", rel="http://opds-spec.org/acquisition/open-access")
    add_subelement_static(entry, "link", href=ia_base_url + str(
        _dict['identifier']) + "/page/cover_medium.jpg", type="image/jpeg", rel="http://opds-spec.org/image")
    add_subelement_static(entry, "link", href=ia_base_url + str(
        _dict['identifier']) + "/page/cover_medium.jpg", type="image/jpeg", rel="http://opds-spec.org/image/thumbnail")

    # === OPDS spec on dates ===
    # OPDS Catalog Entries must include an atom:updated element indicating when the OPDS Catalog Entry was last updated. A dc:issued element should be used to indicate the first publication date of the Publication and must not represent any date related to the OPDS Catalog Entry.

    # issued date
    add_subelement(entry, "issued", "date", _dict, nspace=ns_dcterms)

    # published date
    add_subelement_static(entry, "published",
                          convert_date(_dict["publicdate"]))

    # publisher
    add_subelement(entry, "publisher", "publisher", _dict, nspace=ns_dcterms)

    # updated
    add_subelement_static(entry, "updated", now)

    # language (Note, language is required)
    add_subelement(entry, "language", "language", _dict, nspace=ns_dcterms)

    # Content block
    e_content = etree.SubElement(entry, "content", type="text/html")
    if 'description' in _dict:
        if type(_dict['description']) == str:
            e_content.append(fragment_cleaner(_dict['description']))
        else:
            desc = ('. ').join(_dict['description'])
            e_content.append(fragment_cleaner(desc))
    else:
        print('Warning: No description.')
        errors.append('description')
    e_content_p2 = etree.SubElement(e_content, "p")
    e_content_clio_link = etree.SubElement(
        e_content_p2, "a", href='https://clio.columbia.edu/catalog/' + str(_bibid))
    e_content_clio_link.text = "View catalog record in CLIO."

    # Generic classifcation
    # Audience
    add_subelement_static(entry, "category", term="Adult",
                          label="Adult", scheme="http://schema.org/audience")

    # Nonfiction
    # TODO: check that this applies to all
    add_subelement_static(entry, "category", term="http://librarysimplified.org/terms/fiction/Nonfiction",
                          label="Nonfiction", scheme="http://librarysimplified.org/terms/fiction/")

    # Subjects
    if 'subject' in _dict:
        the_subjects = _dict['subject']
        if type(the_subjects) == str:
            # string, not a list
            add_subelement_static(
                entry, "category", term=the_subjects, label=the_subjects)
        else:
            for s in the_subjects:
                add_subelement_static(entry, "category", term=s, label=s)
    else:
        print('Warning: No subjects.')
        errors.append('subject')

    # End entry and return list of errors/warnings to parent
    return errors


def add_subelement(_parent, _element_name, _source_key, _dict, formated='%s', nspace='', **kwargs):
    # append an element to a parent drawing from given key in given dict. Kwargs are added as attributes.
    if _source_key in _dict:
        if type(_source_key) == list:
            print("Warning: " + _source_key + " has more than one value!")
            errors.append(_source_key)
        else:
            e_elem = etree.SubElement(_parent, nspace + _element_name, kwargs)
            e_elem.text = formated % _dict[_source_key]
    else:
        print('Warning: no *' + _source_key + '* key value!')
        errors.append(_source_key)


def add_subelement_static(_parent, _element_name, _text="", nspace='', **kwargs):
    # append an element to a parent with given text and attributes (kwargs). If no text then creates empty element.
    e_elem = etree.SubElement(_parent, nspace + _element_name, kwargs)
    if _text:
        e_elem.text = _text


def fragment_cleaner(_str):
    x = html.fragment_fromstring(_str, create_parent='p')
    etree.strip_tags(x, '*')
    return x


def convert_date(_datetime):
    # Convert date of format "2020-04-02 12:32:17.628" to ISO
    # d = datetime.strptime(_datetime, '%Y-%m-%d %H:%M:%S.%f')
    d = datetime.strptime(_datetime, '%Y-%m-%d %H:%M:%S')
    return d.isoformat()


if __name__ == "__main__":
    main()
