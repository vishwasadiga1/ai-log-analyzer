from django.shortcuts import render

# Create your views here.

from collections import defaultdict
from sklearn.ensemble import IsolationForest
import numpy as np

def analyze_logs(file_path):
    failed_logins = defaultdict(int)
    alerts = []
    login_counts = []

    with open(file_path, 'r') as f:
        for line in f:
            if "Failed login attempt" in line:
                user = line.split(":")[-1].strip()
                failed_logins[user] += 1
                login_counts.append(failed_logins[user])

                if failed_logins[user] >= 3:
                    alerts.append(f"Multiple failed logins: {user}")

            if "Multiple requests from IP" in line:
                ip = line.split()[-1]
                alerts.append(f"Possible DDoS from {ip}")

    # AI part
    anomalies = []
    if len(login_counts) > 0:
        data = np.array(login_counts).reshape(-1, 1)
        model = IsolationForest(contamination=0.2)
        model.fit(data)
        preds = model.predict(data)

        for i, val in enumerate(preds):
            if val == -1:
                anomalies.append(f"Anomalous login spike detected: {login_counts[i]}")

    return alerts, anomalies

from django.shortcuts import render
from .models import LogFile
import os

def upload_log(request):
    if request.method == 'POST':
        file = request.FILES['logfile']
        log = LogFile.objects.create(file=file)

        file_path = log.file.path
        alerts, anomalies = analyze_logs(file_path)

        return render(request, 'result.html', {
            'alerts': alerts,
            'anomalies': anomalies
        })

    return render(request, 'upload.html')