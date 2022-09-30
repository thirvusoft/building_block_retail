import frappe

def cal_per_hour(doc, actions):
    total_hour= 0
    total_net_hour = 0
    total_hour = doc.administrator_expense + total_hour
    total_net_hour = doc.hour_rate + total_net_hour
    doc.hour_rate = total_hour + total_net_hour