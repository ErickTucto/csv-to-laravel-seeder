from os.path import splitext, basename, abspath, dirname
import csv

template = """{model}::create([
{attributes}
]);
"""


def getFileName(file):
    base = basename(file)
    return splitext(base)[0]


def getAbsolutePath(file):
    return dirname(abspath(file))


def run(csv_file, indented=" " * 4, delimiter=";", model=None,
        attributes=None, has_header=False):
    with open(csv_file, newline='') as csvfile:
        seeder = ""
        file_name = getFileName(csvfile.name)
        model = model or file_name.capitalize()
        include_header = attributes and not has_header
        reader = csv.DictReader(csvfile, delimiter=delimiter)
        for data in reader:
            content = ""
            attributes = attributes or tuple(data)
            if include_header:
                content = "\n".join([
                    '%s"%s" => "%s",' %
                    (indented, attribute, tuple(data.keys())[i])
                    for i, attribute in enumerate(attributes)
                ])
                seeder += template.format(model=model, attributes=content[:-1])
                include_header = False
                content = ""
            content += "\n".join([
                '%s"%s" => "%s",' %
                (indented, attribute, tuple(data.values())[i])
                for i, attribute in enumerate(attributes)
            ])
            seeder += template.format(model=model, attributes=content[:-1])
        seeder_file = "%s/%s.txt" % (getAbsolutePath(csv_file), file_name)
        f = open(seeder_file, "w")
        f.write(seeder)
        f.close()
