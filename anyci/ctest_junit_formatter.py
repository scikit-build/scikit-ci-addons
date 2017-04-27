import os
import sys

from lxml import etree


def main(build_dir):

    tag_file = build_dir + "/Testing/TAG"
    if not os.path.exists(tag_file):
        raise RuntimeError("Missing tag file %s" % tag_file)

    with open(build_dir + "/Testing/TAG", 'r') as tag:
        dir_name = tag.readline().strip()

    test_xml = build_dir + "/Testing/" + dir_name + "/Test.xml"
    if not os.path.exists(test_xml):
        raise RuntimeError("Couldn't find %s" % test_xml)

    xsl_file = os.path.splitext(__file__)[0] + ".xsl"

    with open(xsl_file, 'r') as xsl:
        xml_doc = etree.parse(test_xml)
        xslt_root = etree.XML(xsl.read())
        transform = etree.XSLT(xslt_root)
        result_tree = transform(xml_doc)
        print(result_tree)

if __name__ == "__main__":
    main(sys.argv[1])
