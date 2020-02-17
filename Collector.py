import eel
import json
import os
import platform

'''
#packages needed to shut down and restart localhost if need be
from psutil import process_iter
from signal import SIGKILL
'''

@eel.expose
def ask_python_exp(exp_name):
    experiment_file = open("web/User/Experiments/" + exp_name + ".json", "r")
    experiment_file  = experiment_file.read()
    experiment_json = json.loads(experiment_file)
    eel.python_gives_exp(experiment_json)

@eel.expose
def delete_exp(exp_name):
    os.remove("web/User/Experiments/" + exp_name + ".json")# delete file

@eel.expose
def load_master_json():
    #check if the uber mega file exists yet
    try:
        master_json = open("web/User/master.json", "r")
    except:
        master_json = open("web/kitten/Default/master.json", "r")
    finally:
        master_json = master_json.read()
        master_json = json.loads(master_json)
        eel.load_master_json(master_json)


@eel.expose
def pull_open_collector(username,
                        password,
                        organisation,
                        repository):
    if(organisation == ""):
        organisation = username
    try:
        push_collector(username,
                       password,
                       organisation,
                       repository,
                       "backup before updating from open-collector repository")
        os.system("git remote set-url --push origin https://github.com/" + organisation +"/" + repository + ".git")
        pull_open_collector_only()

    except:
        print("Something went wrong")
    finally:
        print("Attempt to update finished")
        #should trigger restart here

def pull_open_collector_only():
    os.system("remote set-url origin https://github.com/open-collector/open-collector.git")
    os.system("git fetch origin master")
    os.system("git merge -X theirs origin/master --allow-unrelated-histories -m'update from open-collector'")
    if platform.system().lower() == "windows":
        os.system("WindowsCompileCollector.bat")
    #currently mac and linux users have to use python versions.

@eel.expose
def push_collector(username,
                   password,
                   organisation,
                   repository,
                   this_message):
    print("trying to push to the repository")
    if organisation == "":
        organisation = username
    #create repository if that fails
    #os.system("git push https://github.com/open-collector/open-collector")
    try:
        print(this_message)
        os.system("git add .")
        os.system('git commit -m "' + str(this_message) + '"')
        os.system("git push https://" + username + ":" + password + "@github.com/" + organisation + "/" + repository+ ".git")
    except:
        print("looks like I need to create a repository to push to")

        #need to make this a repository
        if(organisation != username):
            create_repository = organisation + "/" + repository
        else :
            create_repository = repository
        os.system('git init')
        os.system('eval "$(ssh-agent -s)"')
        os.system("hub create " + create_repository)
        os.system("git add .")
        os.system("git commit -m 'pushing from local'")
        os.system("git push https://" + username + ":" + password + "@github.com/" + organisation + "/" + repository+ ".git")
        #git config receive.denyCurrentBranch refuse
        #git push --set-upstream py2rm-collector

        #os.system("git push https://" + username + ":" + password + "@github.com/" + organisation + "/" + repository)
    finally:
        print("It all seems to have worked - mostly speaking")




@eel.expose
def rename_experiment(old_name,
                      new_name):
    #rename the experiment json
    #rename the experiment folder
    print("not yet implemented")

@eel.expose
def rename_survey(old_name,
                  new_name):
    try:
        os.rename("web/User/Surveys/" + old_name,
                  "web/User/Surveys/" + new_name)
        eel.update_master_surveys(old_name,
                                  new_name)
    except Exception as err:
        print(err)
        eel.python_bootbox(str(err))



@eel.expose
def request_sheet(experiment,
                  sheet_type,
                  sheet_name):

    if os.path.isfile("web/User/Experiments/" + experiment + "/" + sheet_name):
        sheet_content = open("web/User/Experiments/" + experiment + "/" + sheet_name, "r")
        sheet_content = sheet_content.read()
    else:
        sheet_content = experiment

    eel.receive_sheet(sheet_content,
                      sheet_type,
                      sheet_name)

@eel.expose
def save_data(experiment_name,
              participant_code,
              completion_code,
              responses):
    print("experiment_name")
    print(experiment_name)
    print("participant_code")
    print(participant_code)
    print("responses")
    print(responses)
    if os.path.isdir("web/User/Data") == False:
        os.mkdir("web/User/Data")
    if os.path.isdir("web/User/Data/" + experiment_name) == False:
        os.mkdir("web/User/Data/" + experiment_name)
    experiment_file = open("web/User/Data/" + experiment_name+ "/" + participant_code + "-" + completion_code + ".csv", "w", newline='')
    experiment_file.write(responses)


@eel.expose
def save_experiment(experiment_name,experiment_json):
    errors = ""
    print("trying to save experiment")
    if os.path.isdir("web/User/Experiments") == False:
        os.mkdir("web/User/Experiments")
    print(experiment_name)
    print(json.dumps(experiment_json))
    experiment_file = open("web/User/Experiments/" + experiment_name + ".json", "w")
    experiment_file.write(json.dumps(experiment_json))

    python_message = "Experiment saved"
    eel.python_bootbox(python_message)

    if os.path.isdir("web/User/Experiments/" + experiment_name) == False:
        os.mkdir("web/User/Experiments/" + experiment_name)

    python_message = python_message + "...<br> saving <b>conditions.csv</b>"
    eel.python_bootbox(python_message)
    try:
        this_cond_file = open("web/User/Experiments/" + experiment_name + "/conditions.csv", "w", newline='')
        this_cond_file.write(experiment_json["python_conditions"])
    except:
        errors += "...<br><span class='text-danger'>Error when trying to save <b>conditions.csv</b> - is the file open on your computer?</span>"
        eel.python_bootbox(python_message)
    finally:
        print("moving on")


    for this_proc in experiment_json["python_procs"].keys():
        python_message = python_message + "...<br> saving the procedure <b>" + this_proc + "</b>"
        eel.python_bootbox(python_message)
        print(this_proc)
        try:
            this_proc_file = open("web/User/Experiments/" + experiment_name + "/" + this_proc, "w", newline='')
            this_proc_file.write(experiment_json["python_procs"][this_proc])
        except:
            errors += "...<br><span class='text-danger'>Error when trying to save <b>" + \
                              this_proc + \
                              "</b> - is the file open on your computer?</span>"
            eel.python_bootbox(python_message)
        finally:
            print("moving on")

    for this_stim in experiment_json["python_stims"].keys():
        python_message = python_message + "...<br> saving the stimuli <b>" + this_stim + "</b>"
        eel.python_bootbox(python_message)
        print(this_stim)
        try:
            this_stim_file = open("web/User/Experiments/" + experiment_name + "/" + this_stim, "w", newline='')
            this_stim_file.write(experiment_json["python_stims"][this_stim])
        except:
            print("error here");
            errors += "...<br><span class='text-danger'>Error when trying to save <b>" + \
                              this_stim + \
                              "</b> - is the file open on your computer?</span>"
            eel.python_bootbox(python_message)
        finally:
            print("moving on")

    if errors == "":
        eel.python_hide_bb()
    else:
        eel.python_bootbox(python_message + errors)

@eel.expose
def save_master_json(master_json):
    #detect if the "User" folder exists yet
    if os.path.isdir("web/User") == False:
        os.mkdir("web/User")
    master_file = open("web/User/master.json", "w")
    master_file.write(json.dumps(master_json))

@eel.expose
def save_survey(survey_name,
                survey_content):
    #detect if the "User" folder exists yet
    if os.path.isdir("web/User/Surveys") == False:
        os.mkdir("web/User/Surveys")
    survey_file = open("web/User/Surveys/" + survey_name, "w", newline='')
    survey_file.write(survey_content)


####################
# Start Collector ##
####################

if os.path.isdir("web") == False:

    # more code here



    # check if github is installed

    pull_open_collector_only()



eel.init('web') #allowed_extensions=[".js",".html"]


'''
for proc in process_iter():
    for conns in proc.get_connections(kind='inet'):
        if conns.laddr[1] == 8000:
            proc.send_signal(SIGKILL)
            continue
'''
eel.start('kitten/index.html', port=8000)

