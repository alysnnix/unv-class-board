from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView
from core.models import Teacher, ClassGroup, SchoolSegment
from attendance.models import TeacherAbsence, TeacherSubstitution
from django.db.models import Count
from django.db.models.functions import ExtractMonth, ExtractIsoWeekDay
from django.utils import timezone
import json

class DashboardView(TemplateView):
    template_name = 'core/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # 1. Real Statistics
        context['teachers_count'] = Teacher.objects.count()
        context['classes_count'] = ClassGroup.objects.count()
        context['segments_count'] = SchoolSegment.objects.count()

        # 2. Bar Chart Logic (Absences by Day of the Week)
        # IsoWeekDay: 1=Monday, 2=Tuesday, ..., 7=Sunday
        absences_by_day = TeacherAbsence.objects.annotate(
            day_of_week=ExtractIsoWeekDay('start_date')
        ).values('day_of_week').annotate(total=Count('id')).order_by('day_of_week')
        
        # Initialize dictionary with all business days starting at 0
        business_days = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0} # Monday to Friday
        for absence in absences_by_day:
            if absence['day_of_week'] in business_days:
                business_days[absence['day_of_week']] = absence['total']
                
        context['bar_labels'] = json.dumps(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
        context['bar_data'] = json.dumps(list(business_days.values()))
        
        # 3. Pie Chart Logic (Classes by Period)
        classes_by_period = ClassGroup.objects.values('period__name').annotate(total=Count('id'))
        
        pie_labels = []
        pie_data = []
        for c in classes_by_period:
            period_name = c['period__name'] if c['period__name'] else "No Period"
            pie_labels.append(period_name)
            pie_data.append(c['total'])
            
        context['pie_labels'] = json.dumps(pie_labels if pie_labels else ["No Data"])
        context['pie_data'] = json.dumps(pie_data if pie_data else [1])
        
        return context

class LineChartJSONView(BaseLineChartView):
    
    def get_months_data(self):
        current_year = timezone.now().year
        
        absences = TeacherAbsence.objects.filter(start_date__year=current_year).annotate(
            month=ExtractMonth('start_date')
        ).values('month').annotate(total=Count('id')).order_by('month')
        
        subs = TeacherSubstitution.objects.filter(start_date__year=current_year).annotate(
            month=ExtractMonth('start_date')
        ).values('month').annotate(total=Count('id')).order_by('month')
        
        current_month = timezone.now().month
        months_list = []
        labels = []
        
        for i in range(5, -1, -1):
            m = current_month - i
            if m <= 0:
                m += 12 
            months_list.append(m)
            month_name = {
                1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
            }.get(m, str(m))
            labels.append(month_name)
            
        absences_data = [0] * 6
        subs_data = [0] * 6
        
        for a in absences:
            if a['month'] in months_list:
                idx = months_list.index(a['month'])
                absences_data[idx] = a['total']
                
        for s in subs:
            if s['month'] in months_list:
                idx = months_list.index(s['month'])
                subs_data[idx] = s['total']
                
        return labels, absences_data, subs_data

    def get_labels(self):
        labels, _, _ = self.get_months_data()
        return labels

    def get_providers(self):
        return ["Registered Absences", "Substitutions Done"]

    def get_data(self):
        _, absences, subs = self.get_months_data()
        return [
            absences,
            subs
        ]

dashboard_view = DashboardView.as_view()
line_chart_json = LineChartJSONView.as_view()