from django.shortcuts import render
from . import forms
from django.views.generic.edit import UpdateView

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def climate(edw1,alt1):
    if (edw1<0 or alt1 <0 or alt1>90 or edw1>120000):
        result_alpha = 0
        return result_alpha


    # New Antecedent/Consequent objects hold universe variables and membership
    # functions
    edw = ctrl.Antecedent(np.arange(0, 120001, 1), 'Daylight')
    alt = ctrl.Antecedent(np.arange(-.1, 91, 1), 'Solar altitude')
    alpha = ctrl.Consequent(np.arange(0, 1.1, .1), 'Blind Position')

    # Auto-membership function population is possible with .automf(3, 5, or 7)

    edw['l']=fuzz.trapmf(edw.universe, [0, 0, 10000, 20000])
    edw['h']=fuzz.trapmf(edw.universe, [10000, 20000, 50000, 50000])
    edw['vh']=fuzz.trapmf(edw.universe, [50000, 100000, 120000, 120000])

    alt['l']=fuzz.trimf(alt.universe, [0, 15, 30])
    alt['m']=fuzz.trimf(alt.universe, [15, 30, 60])
    alt['h']=fuzz.trimf(alt.universe, [30, 60, 90])

    # Custom membership functions can be built interactively with a familiar,
    # Pythonic API
    alpha['vl'] = fuzz.trimf(alpha.universe, [0, 0, 0])
    alpha['l'] = fuzz.trimf(alpha.universe, [0, 0.2, 0.4])
    alpha['m'] = fuzz.trimf(alpha.universe, [0.2, 0.4, 0.6])
    alpha['h'] = fuzz.trimf(alpha.universe, [0.4, 0.7, 1])
    alpha['vh'] = fuzz.trimf(alpha.universe, [1, 1, 1])

    rule1 = ctrl.Rule(edw['l'] & alt['l'], alpha['vh'])
    rule2 = ctrl.Rule(edw['h'] & alt['l'], alpha['l'])
    rule3 = ctrl.Rule(edw['vh'] & alt['l'], alpha['vl'])
    rule4 = ctrl.Rule(edw['l'] & alt['m'], alpha['vh'])
    rule5 = ctrl.Rule(edw['h'] & alt['m'], alpha['m'])
    rule6 = ctrl.Rule(edw['vh'] & alt['m'], alpha['vl'])
    rule7 = ctrl.Rule(edw['l'] & alt['h'], alpha['vh'])
    rule8 = ctrl.Rule(edw['h'] & alt['h'], alpha['h'])
    rule9 = ctrl.Rule(edw['vh'] & alt['h'], alpha['vl'])

    blind_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
    blind = ctrl.ControlSystemSimulation(blind_ctrl)

    # Pass inputs to the ControlSystem using Antecedent labels with Pythonic API
    # Note: if you like passing many inputs all at once, use .inputs(dict_of_data)
    blind.input['Daylight'] = edw1
    blind.input['Solar altitude'] = alt1
    # Crunch the numbers
    blind.compute()

    result_alpha = blind.output['Blind Position']
    return result_alpha


def form_name_view(request):
      cond = False
      form = forms.FormName()

      if request.method == 'POST':
          form = forms.FormName(request.POST)

      if form.is_valid():
          inp1 = form.cleaned_data['edw']
          inp2 = form.cleaned_data['alt']
          cond = inp1 >-1 and inp1 < 120001 and inp2 < 91 and inp2 >-1
          print(cond)
          res=round(climate(inp1,inp2)*100,3)
          print(res)

      if cond:
          return render(request,'myapp/visualcomfort_form.html',{'form':form, 'res':res })
      else:
          return render(request,'myapp/visualcomfort_form.html',{'form':form, 'res':"Please enter a value within the range" })
