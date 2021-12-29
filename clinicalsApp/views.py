from django.shortcuts import render,redirect
from clinicalsApp.models import Patient,ClinicalData
from django.views.generic import ListView,CreateView,DeleteView,UpdateView
from django.urls import reverse_lazy
from clinicalsApp.forms import ClinicalDataForm
# Create your views here.
class PatientListView(ListView):
    model= Patient

class PatientCreateView(CreateView):
    model = Patient
    fields=('firstName','lastName','age')
    success_url=reverse_lazy('index')

class PatientUpdateView(UpdateView):
    model = Patient
    fields=('firstName','lastName','age')
    success_url=reverse_lazy('index')

class PatientDeleteView(DeleteView):
    model = Patient
    success_url=reverse_lazy('index')

def addData(request,**kwargs):
    form =ClinicalDataForm()
    patient = Patient.objects.get(id=kwargs['pk'])
    if request.method =='POST':
        form  = ClinicalDataForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/')
    return render(request,'clinicalsApp/clinicaldata_form.html',{'form':form,'patient':patient})

def analyse(request,**kwargs):
    data =ClinicalData.objects.filter(patient_id =kwargs['pk'])
    responseData = []
    for eachEntry in data:
        if eachEntry.componentName=='hw':
            heightAndWeight = eachEntry.componentValue.split('/')
            if len(heightAndWeight)>1:
                feetToMeters = float(heightAndWeight[0])* 0.4536
                BMI = (float(heightAndWeight[1]))/(feetToMeters*feetToMeters)
                bmiEntry=ClinicalData()
                bmiEntry.componentName='BMI'
                bmiEntry.componentValue=BMI
                responseData.append(bmiEntry)
        responseData.append(eachEntry)

    return render(request, 'clinicalsApp/generateReport.html',{'data':responseData})
