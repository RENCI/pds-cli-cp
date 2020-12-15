from birthDate import *
from tx.dateutils.utils import strtodate
from dateutil.relativedelta import relativedelta
height_unit = "m"
weight_unit = "kg"
bmi_unit = "kg/m^2"
x = 10
y = 10
study_start = "2010-01-01T00:00:00Z"
study_end = "2011-01-01T00:00:00Z"
for pid in patientIds:
    patient = get_patient(patient_id=pid, fhir=data)
    birthDate = birthDate(patient)
#    birthTime = birthTime(patient)
    sex = sex(patient)
    return {
      "values": [
          {'id':"PATID",'variableValue': {'value': pid}},
          {'id':"BIRTH_DATE",**birthDate},
          {'id':"BIRTH_TIME",'variableValue': {'value': '00:00'}},
          {'id':"SEX",**sex} 
      ]
    }
