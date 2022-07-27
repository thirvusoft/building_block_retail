import frappe 

def validate(doc, event):
    for i in doc.operations:
        if(i.time_in_mins == 0):i.time_in_mins=10