#!/usr/bin/python

import xmltodict
import os
import re
import sys
import json



def get_files(d):
        files = []
        for f in os.listdir(d):
                if re.match('.*\.plan\.xml$',f):
                        files.append(f)

        return files



def get_xml(f):
        xml = open(f, "r").read()
        try:
                return xmltodict.parse(xml)
        except:
                print("ERROR parsing %s" % (f))
                sys.exit(1)


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



def check_plan(f, p = False):
        obj = get_xml(f)
        number_of_variables_definded = int(check_variables_definition(obj).split(':')[0])
        variables_definded = check_variables_definition(obj).split(':')[1]

        number_of_variables_assignment = int(check_variables_assignment(obj))

        if p:
                print("Defined variables found in %s: %s" %(f, str(number_of_variables_definded)))
                print("Assignment variables found in %s: %s" %(f, str(number_of_variables_assignment)))
                print("")

        return str(number_of_variables_definded) + ":" + str(number_of_variables_assignment) + ":" + variables_definded



if __name__ == "__main__":
        d = "deployment"
        cr = 0

        for f in get_files(d):
                df = d + "/" + f

                if 'last_file_check' not in locals():
                        last_file_check = check_plan(df, True)
                        last_file = df
                else:
                        if last_file_check != check_plan(df, True):
                                print("Current file %s\n\t%s\n\ndiverges from last file %s\n\t%s" % (df, check_plan(df).split(':')[2], last_file, last_file_check.split(':')[2]))
                                sys.exit(1)

                        last_file_check = check_plan(df)
                        last_file = df

        sys.exit(int(cr))
