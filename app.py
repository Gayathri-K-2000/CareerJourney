from flask import Flask, jsonify,request
import numpy as np
import pandas as pd
from flask_httpauth import HTTPBasicAuth

import json
from pandas import json_normalize

app = Flask(__name__)
auth = HTTPBasicAuth()

@auth.verify_password
def authenticate(username, password):
    if username and password:
        if username == 'admin' and password == 'admin':
            return True
        else:
            return False
    return False
    
@app.route("/path", methods=['POST'])
@auth.login_required
def predict():
    request_data = request.get_json()

    sourcejobid = request.args.get('sourcejobid')
    targetjobid = request.args.get('targetjobid')
    flag = request.args.get('flag')
    if(flag=="1"):
        inpskills = request_data['Skills']
    df = pd.read_csv('jobroles.csv')
    df = df.astype('str')

    #Source and target grades
    dfseid= df.loc[df['JobID'] == sourcejobid]
    sourceGrade= list(set(dfseid["Grade"]))[0]
    dftid= df.loc[df['JobID'] == targetjobid]
    targetGrade= list(set(dftid["Grade"]))[0]

    dfseeid= df.loc[df['JobID'] == sourcejobid]
    ssector= list(set(dfseeid["Sector"]))[0]
    dfsetid= df.loc[df['JobID'] == targetjobid]
    tsector= list(set(dfsetid["Sector"]))[0]
    out=[]



    comp=[]
    sourcejobids= []
    sourcejobids.append(sourcejobid)

    dfseo= df.loc[df['JobID'] == sourcejobid]
    sjobtitle= str(list(set(dfseo["JobRole"]))[0])
    resDicts=dict(JobId=sourcejobid, Jobtitle= sjobtitle, Sector= ssector, CommonSkills="0", MatchSkillsScore= 0, MatchCompetencyScore= 00, MatchScore= 00)
    rs=[]
    rs.append(resDicts)
    out.append(dict(grade= sourceGrade,results= rs ))
    if(int(sourceGrade)<int(targetGrade)):
        for k in range (int(sourceGrade), int(targetGrade)):
                        print("grade ",k)
                        result=[]

                        if(ssector==tsector):
                            dft= df.loc[(df['Grade'] == str(k)) & (df['JobID'] != sourcejobid) & ((df['Sector'] == ssector) |(df['Sector'] == tsector))]
                            if(str(k)==str(sourceGrade)):
                                continue
                        else:
                            dft= df.loc[(df['Grade'] == str(k)) & (df['JobID'] != sourcejobid) & (df['Sector'] == tsector)]
                        if(not sourcejobids):
                            dfide= df.loc[df['JobID'] == src]
                        else:
                            dfide= df.loc[df['JobID'] == sourcejobids[0]]
                            src=sourcejobids[0]
                        
                        inpskills= dfide["Skill"]
                        jobids=list(set(dft["JobID"]))
                        print(jobids)
                        if(not jobids):
                            dft= df.loc[(df['Grade'] == str(k)) & (df['JobID'] != sourcejobid) & ((df['Sector'] == ssector) |(df['Sector'] == tsector))]
                            jobids=list(set(dft["JobID"]))
                            print(jobids)
                      
                        
                        for jid in jobids:
                            dfse= dft.loc[(dft['JobID'] == jid)]
                            eachskills= dfse["Skill"]

                            skillslist1_set = set(inpskills)
                            intersection = skillslist1_set.intersection(eachskills)

                            intersection_skills = list(intersection)

                            common = len(intersection_skills)
                            match= common / len(eachskills)
                            if(common>=10):
                                if(jid in list(set(dft["JobID"]))):
                                    jobid=jid
                                dfje= dfse.loc[dfse['Grade'] == str(k)]
                                dfn= dfje.loc[dfje['JobID'] == str(jobid)]
                                jobtitle= list(set(dfn["JobRole"]))
                                sector= list(set(dfn["Sector"]))

                                resDict=dict(JobId=jobid,Position= jobtitle[0], Sector= sector[0],CommonSkills=intersection_skills, MatchSkillsScore= match, MatchCompetencyScore= 0, MatchScore= common)
                                result.append(resDict)
                                print(result)
 
                            elif(not result):  
                                    if(jid in list(set(dft["JobID"]))):
                                        jobid=jid
                                    dfje= dfse.loc[dfse['Grade'] == str(k)]
                                    dfn= dfje.loc[dfje['JobID'] == str(jobid)]
                                    jobtitle= list(set(dfn["JobRole"]))
                                    sector= list(set(dfn["Sector"]))
                                    resDict=dict(JobId=jid,Position= jobtitle[0], Sector= sector[0],CommonSkills=intersection_skills, MatchSkillsScore= match, MatchCompetencyScore= 0, MatchScore= common)
                                    result.append(resDict)
                                    print(result)
                            else:
                                    if(jid in list(set(dft["JobID"]))):
                                        jobid=jid
                                    dfje= dfse.loc[dfse['Grade'] == str(k)]
                                    dfn= dfje.loc[dfje['JobID'] == str(jobid)]
                                    jobtitle= list(set(dfn["JobRole"]))
                                    sector= list(set(dfn["Sector"]))
                                    resDict=dict(JobId=jid,Position= jobtitle[0], Sector= sector[0],CommonSkills=intersection_skills, MatchSkillsScore= match, MatchCompetencyScore= 0, MatchScore= common)
                                    result.append(resDict)
                                    print(result)
                        out.append(dict(grade= k,results= sorted(result, key=lambda k: k["MatchScore"],reverse=True)[0:3] ))
                    
                        sourcejobids= []
                        for l in range(0,len(sorted(result, key=lambda k: k["MatchScore"],reverse=True)[0:3])):
                                    print(out[-1]["results"][l]['JobId'])
                                    sourcejobids.append(out[-1]["results"][l]['JobId'])
                        print(list(set(sourcejobids)))
    
    result1=[]
    pdfid= df.loc[df['JobID'] == str(sourcejobids[0])]
    pinpskills= pdfid["Skill"]
    ndfid= df.loc[df['JobID'] == targetjobid]
    ninpskills= ndfid["Skill"]

    skillslist1_set = set(pinpskills)
    intersection = skillslist1_set.intersection(ninpskills)

    intersection_skillst = list(intersection)

    commont = len(intersection_skillst)
    print(commont)
    matcht= commont / len(ninpskills)
    dft= df.loc[df['JobID'] == targetjobid]
    jobtitle= str(list(set(dft["JobRole"]))[0])
    resDict1=dict(JobId=targetjobid, Position= jobtitle, CommonSkills=intersection_skillst, MatchSkillsScore= matcht, MatchCompetencyScore= 0, MatchScore= commont)
    result1.append(resDict1)

    dfe=df.loc[df['JobID'] == str(targetjobid)]
    out.append(dict(grade=list(set(dfe["Grade"]))[0],results= result1))
    return jsonify(output=out)

if __name__ == '__main__':
    app.run(debug=True)
