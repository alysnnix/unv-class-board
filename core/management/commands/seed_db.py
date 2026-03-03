import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from core.models import Subject, Teacher, Justification, SchoolSegment, SchoolPeriod, ClassGroup
from schedule.models import Schedule
from attendance.models import TeacherAbsence, TeacherSubstitution
from communication.models import Message

class Command(BaseCommand):
    help = 'Populates the database with realistic fake data for testing and UI validation.'

    def handle(self, *args, **kwargs):
        fake = Faker('pt_BR')  # Using Portuguese locale to generate Brazilian names and phones
        self.stdout.write(self.style.WARNING('Starting database population...'))

        # 1. Create Justifications
        justifications_list = [
            "Motivos Médicos (Atestado)",
            "Problemas Pessoais",
            "Licença Maternidade/Paternidade",
            "Trânsito/Acidente",
            "Luto",
            "Convocações Legais/Justiça"
        ]
        justifications = []
        for name in justifications_list:
            obj, created = Justification.objects.get_or_create(name=name)
            justifications.append(obj)
        self.stdout.write(self.style.SUCCESS(f'Created {len(justifications)} Justifications.'))

        # 2. Create School Segments
        segments_list = ["Ensino Infantil", "Ensino Fundamental I", "Ensino Fundamental II", "Ensino Médio"]
        segments = []
        for name in segments_list:
            obj, created = SchoolSegment.objects.get_or_create(name=name)
            segments.append(obj)
        self.stdout.write(self.style.SUCCESS(f'Created {len(segments)} School Segments.'))

        # 3. Create School Periods
        periods_list = ["Manhã", "Tarde", "Noite", "Integral"]
        periods = []
        for name in periods_list:
            obj, created = SchoolPeriod.objects.get_or_create(name=name)
            periods.append(obj)
        self.stdout.write(self.style.SUCCESS(f'Created {len(periods)} School Periods.'))

        # 4. Create Subjects
        subjects_list = ["Matemática", "Português", "História", "Geografia", "Ciências", "Física", "Química", "Biologia", "Inglês", "Educação Física", "Artes"]
        subjects = []
        for name in subjects_list:
            obj, created = Subject.objects.get_or_create(name=name)
            subjects.append(obj)
        self.stdout.write(self.style.SUCCESS(f'Created {len(subjects)} Subjects.'))

        # 5. Create Class Groups
        class_groups = []
        for i in range(1, 21):
            segment = random.choice(segments)
            period = random.choice(periods)
            # Create a name like "1º Ano A" or "9º Ano C"
            grade = random.randint(1, 9)
            letter = random.choice(['A', 'B', 'C', 'D'])
            name = f"{grade}º Ano {letter} - {segment.name.split()[-1]}"
            obj, created = ClassGroup.objects.get_or_create(
                name=name,
                segment=segment,
                period=period
            )
            class_groups.append(obj)
        self.stdout.write(self.style.SUCCESS(f'Created {len(class_groups)} Class Groups.'))

        # 6. Create Teachers
        teachers = []
        for _ in range(40):
            # Generate a phone number that matches the RegexValidator: '^\+?1?\d{9,15}$'
            # Let's generate a valid Brazilian mobile phone number: +5511999999999
            area_code = random.randint(11, 99)
            number = random.randint(900000000, 999999999)
            phone = f"+55{area_code}{number}"
            
            obj = Teacher.objects.create(
                name=fake.name(),
                phone=phone,
                is_substitute=random.choice([True, False, False, False]) # 25% chance of being substitute
            )
            # Assign 1 to 3 random subjects to the teacher
            assigned_subjects = random.sample(subjects, k=random.randint(1, 3))
            obj.subjects.set(assigned_subjects)
            teachers.append(obj)
        self.stdout.write(self.style.SUCCESS(f'Created {len(teachers)} Teachers.'))

        # 7. Create Schedules
        days_of_week = [c[0] for c in Schedule.DAY_OF_WEEK_CHOICES]
        # Times slots: 07:00, 08:00, 09:00, 10:00, 11:00
        time_slots = [
            ("07:00:00", "08:00:00"),
            ("08:00:00", "09:00:00"),
            ("09:00:00", "10:00:00"),
            ("10:00:00", "11:00:00"),
            ("11:00:00", "12:00:00")
        ]
        
        schedules_created = 0
        # We will attempt to create some schedules, catching validation errors
        for class_group in class_groups:
            for day in days_of_week:
                # 3 classes per day per class_group
                daily_slots = random.sample(time_slots, 3)
                for start_t, end_t in daily_slots:
                    teacher = random.choice(teachers)
                    subject = random.choice(list(teacher.subjects.all()))
                    
                    try:
                        Schedule.objects.create(
                            day_of_week=day,
                            class_group=class_group,
                            teacher=teacher,
                            subject=subject,
                            start_time=start_t,
                            end_time=end_t
                        )
                        schedules_created += 1
                    except Exception:
                        # Ignore unique constraint violations (e.g. teacher already busy)
                        pass
        self.stdout.write(self.style.SUCCESS(f'Created {schedules_created} Schedules.'))

        # 8. Create Absences and Substitutions
        absences_created = 0
        subs_created = 0
        today = timezone.now().date()
        
        for _ in range(50):
            teacher = random.choice(teachers)
            # Random date within the last 6 months to populate the chart
            days_ago = random.randint(0, 180)
            start_date = today - timedelta(days=days_ago)
            end_date = start_date + timedelta(days=random.randint(0, 3)) # Absent for 1 to 4 days
            
            absence = TeacherAbsence.objects.create(
                start_date=start_date,
                end_date=end_date,
                teacher=teacher,
                justification=random.choice(justifications)
            )
            absences_created += 1
            
            # 70% chance of getting a substitute
            if random.random() < 0.7:
                sub_candidates = [t for t in teachers if t != teacher and t.is_substitute]
                if not sub_candidates:
                    sub_candidates = [t for t in teachers if t != teacher] # Anyone if no subs available
                
                substitute = random.choice(sub_candidates)
                try:
                    TeacherSubstitution.objects.create(
                        start_date=start_date,
                        end_date=end_date,
                        absent_teacher=teacher,
                        substitute_teacher=substitute
                    )
                    subs_created += 1
                except Exception:
                    pass
        self.stdout.write(self.style.SUCCESS(f'Created {absences_created} Absences and {subs_created} Substitutions.'))

        # 9. Create Messages
        message_types = [c[0] for c in Message.MESSAGE_TYPES]
        messages_created = 0
        for _ in range(20):
            days_ago = random.randint(0, 60)
            date = today - timedelta(days=days_ago)
            
            msg = Message.objects.create(
                message_type=random.choice(message_types),
                date=date,
                description=fake.text(max_nb_chars=200)
            )
            
            # Link to some class groups and teachers
            msg.class_groups.set(random.sample(class_groups, k=random.randint(0, 3)))
            msg.teachers.set(random.sample(teachers, k=random.randint(0, 5)))
            messages_created += 1
            
        self.stdout.write(self.style.SUCCESS(f'Created {messages_created} Messages.'))

        self.stdout.write(self.style.SUCCESS('🎉 Database population completed successfully!'))
