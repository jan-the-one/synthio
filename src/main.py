import getopt, sys
from benchgen.weaver.cpp_weaver import CppWeaver
from benchgen.user_subsys.exp import Experiment, EXP_TYPE
from benchgen.user_subsys.fw import Framework, FW_TYPE
from benchgen.user_subsys.core import SynthIO

GENERATE_COMMAND = "generate-benchmark"
COMPILE_GADGETS = "derive-gadgets"
WEAVE_ONLY = "weave"
EXPERIMENT= "experiment"
#if an experiment command is provided, we select a different instance of the framework. 
#we might want to create an abstract class for the framework overall.
#that different instances should not handle any gadget compilations. It simply does "manipulated" weavings + second-level derivations

def main():
    
    template_name = ""
    fw = Framework()

    if len(sys.argv) < 2:
        print("No command provided!")
        exit(1)

    command = sys.argv[1].lower()
    
    if command == COMPILE_GADGETS:
        fw.mode = FW_TYPE.COMPILE_ONLY
    elif command == GENERATE_COMMAND or command == WEAVE_ONLY: 
        derive_second_level = False
        argv = sys.argv[2:]
        try:
            opts, _ = getopt.getopt(argv, "dt:", ["derive", "template-name="])
        except:
            print("Could not parse options!")
            exit(3)
            
        for opt, arg in opts:
            if opt in ['-t', '--template-name']:
                template_name = arg
            if opt in ['-d', '--derive']:
                derive_second_level = True

        if template_name == "":
            print("No Template name given! Please provide a name by adding `-t <template_name>`")
            exit(3)

        if command == GENERATE_COMMAND:
            fw.mode = FW_TYPE.FULL_RUN
        else: 
            fw.mode = FW_TYPE.WEAVE_ONLY

        fw.weaver = CppWeaver()
        fw.with_second_level = derive_second_level
        fw.target_template = template_name

    elif command == EXPERIMENT:
        
        fw = Experiment() #override previous instantiation
        gv_hash = ""
        #TODO add "-n=" option so that the user can specify a number of experiments. This is useful for consistency measurements.
        argv = sys.argv[2:]
        try:
            opts, _ = getopt.getopt(argv, "b:ic:t:o:", ["impact-mapping", "consistency=", "template", "combination="])
        except:
            print("Could not parse options. Make sure to provide a template name by adding <template_name> after one of the options -[bictp]")
            exit(3)

        for opt, arg in opts:
            if opt in ['-i', '--impact-mapping']:
                fw.mode = EXP_TYPE.IMPACT_MAPPING
                break
            if opt in ['-c', '--consistency']:
                fw.mode = EXP_TYPE.CONSISTENCY
                template_name = arg
                break
            if opt in ['-b', '--baseline']:
                fw.mode = EXP_TYPE.BASELINE
                template_name = arg
                break
            if opt in ['-t', '--template']:
                fw.mode = EXP_TYPE.TEMPLATE
                template_name = arg
                break
            if opt in ['-o', '--combination']:
                fw.mode = EXP_TYPE.COMBINATION
                template_name=arg
                break

        if fw.mode != EXP_TYPE.IMPACT_MAPPING and template_name == "":
            print("No Template name given! Please provide a name by using `-c <template_name>` or `-i <template_name>`")
            exit(3)

        fw.weaver = CppWeaver()
        fw.target_template = template_name
        fw.with_second_level = True

    else:
        print("Unknown command!")
        exit(2)

    fw.run()

if __name__ == "__main__":
    main()
    