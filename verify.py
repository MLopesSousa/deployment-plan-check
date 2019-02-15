#!/usr/bin/python



import xmltodict
import os
import re
import sys
import json



def get_xml_files(d):
        files = []
        for f in os.listdir(d):
                if re.match('.*\.plan\.xml$',f):
                        files.append(f)

        return files



def get_prop_files(d):
        files = []
        for f in os.listdir(d):
                if re.match('.*\.properties$',f):
                        files.append(f)

        return files



def get_xml(f):
        xml = open(f, "r").read()
        try:
                return xmltodict.parse(xml)
        except:
                print("ERROR parsing %s" % (f))



def check_variables_definition(obj):
        defined_variables = obj['deployment-plan']['variable-definition']['variable']
        defined_variables_hash = []
        for variable in defined_variables:
                defined_variables_hash.append(variable['name'])

        return str(len(defined_variables)) + ":" + " ".join(sorted(defined_variables_hash))



def check_variables_assignment(obj):
        defined_assignment = 0
        for module_descriptor in obj['deployment-plan']['module-override']['module-descriptor']:
                if not module_descriptor.get('variable-assignment') == None:
                        defined_assignment+= len(module_descriptor['variable-assignment'])

        return str(defined_assignment)



def check_xml_plan(f, p = False):
        obj = get_xml(f)
        number_of_variables_definded = int(check_variables_definition(obj).split(':')[0])
        variables_definded = check_variables_definition(obj).split(':')[1]

        number_of_variables_assignment = int(check_variables_assignment(obj))

        if p:
                print("Defined variables found in %s: %s" %(f, str(number_of_variables_definded)))
                print("Assignment variables found in %s: %s" %(f, str(number_of_variables_assignment)))
                print("")

        return str(number_of_variables_definded) + ":" + str(number_of_variables_assignment) + ":" + variables_definded



def check_prop_plan(f, p = False):
        variables = []

        for line in open(f, "r").read().splitlines():
                if len(line) > 1 and not re.match('^#', line):
                        variables.append(line.split('=')[0])

        number_of_variables_definded = len(variables)
        variables_definded = " ".join(sorted(variables))

        if p:
                print("Defined variables found in %s: %s" %(f, str(number_of_variables_definded)))
                print("")

        return str(number_of_variables_definded) + ":" + variables_definded



def  check_xml(d):
        for f in get_xml_files(d):
                df = d + "/" + f

                if 'last_file_check' not in locals():
                        last_file_check = check_xml_plan(df, True)
                        last_file = df
                else:
                        if last_file_check != check_xml_plan(df, True):
                                print("Current file %s\n\t%s\n\ndiverges from last file %s\n\t%s" % (df, check_xml_plan(df).split(':')[2], last_file, last_file_check.split(':')[2]))
                                return False

                        last_file_check = check_xml_plan(df)
                        last_file = df

        return True


def check_prop(d):
        for f in get_prop_files(d):
                df = d + "/" + f

                if 'last_file_check' not in locals():
                        last_file_check = check_prop_plan(df, True)
                        last_file = df
                else:
                        if last_file_check != check_prop_plan(df, True):
                                print("Current file %s\n\t%s\n\ndiverges from last file %s\n\t%s" % (df, check_prop_plan(df).split(':')[1], last_file, last_file_check.split(':')[1]))
                                return False

                        last_file_check = check_prop_plan(df)
                        last_file = df

        return True



if __name__ == "__main__":
        r = 0
        d = str(sys.argv[1])

        if not os.path.exists(d):
                print("Directory " + d + " doesn't exist")
                sys.exit(1)

        types = str(sys.argv[2])

        for check in types.split(':'):
                if check == "xml":
                        if not check_xml(d):
                                r = 1

                if check == "prop":
                        if not check_prop(d):
                                r = 1

        sys.exit(r)
