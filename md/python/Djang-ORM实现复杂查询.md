### models
```
 from django.db import models

class Student(models.Model):
    """学生表"""
    name = models.CharField(max_length=100)
    gender = models.SmallIntegerField()

    class Meta:
        db_table = 'student'

class Course(models.Model):
    """课程表"""
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey("Teacher",on_delete=models.SET_NULL,null=True)
    class Meta:
        db_table = 'course'

class Score(models.Model):
    """分数表"""
    student = models.ForeignKey("Student",on_delete=models.CASCADE)
    course = models.ForeignKey("Course",on_delete=models.CASCADE)
    number = models.FloatField()

    class Meta:
        db_table = 'score'

class Teacher(models.Model):
    """老师表"""
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'teacher'
```
### 查询

查询平均成绩大于60分的同学的id和平均成绩
```
Student.objects.annotate(avg=Avg("score__number")).filter(avg__gte=60).values("id","avg")
```
查询所有同学的id、姓名、选课的数、总成绩
```
	Student.objects.annotate(course_num=Count("score__course"),score_count=sum("score__number")).values("id","name","course_num","score_count")
```
查询姓“李”的老师的个数
```
Teacher.objects.filter(name__startswith="李").count()
```
查询没学过“黄老师”课的同学的id、姓名
```
Student.objects.exclude(score_course_teacher_name="黄老师").values("id","name")
```
查询学过课程id为1和2的所有同学的id、姓名
```
Student.objects.filter(score_course__in=[1,2]).dictinct.values("id","name")
```
查询学过“黄老师”所教的所有课的同学的学号、姓名
```
Student.objects.annotate(nums=Count("score__course",filter=Q(score__course__teacher__name='黄老师')))
.filter(nums=Course.objects.filter(teacher__name='黄老师').count()).values('id','name')
```
查询所有课程成绩小于60分的同学的id和姓名
```
Student.objects.exclude(score_number—__gt=60)
```
查询没有学全所有课的同学的id、姓名
```
Student.objects.annotate(num=Count(F("score_course"))).filter(num__lt=Course.objects.count()).values("id","name")
```
查询所有学生的姓名、平均分，并且按照平均分从高到低排序
```
Student.objects.annotate(avg=Avg("score_number")).order_by("-avg").values("name","avg")
```
查询各科成绩的最高和最低分，以如下形式显示：课程ID，课程名称，最高分，最低分
```
Course.objects.annotate(min=Min("score_number"),max=Max("score_number")).values("id","name","max","min")
```
查询每门课程的平均成绩，按照平均成绩进行排序
```
Course.objects.annotate(avg=Avg("score_number")).order_by("avg").values("id","name","avg")
```
统计总共有多少女生，多少男生
```
Student.objects.aggreagte(male_num=Count("gender",filter=Q(gender=1)),female_num=Count("gender",filter=Q(gender=2)))
```
将“黄老师”的每一门课程都在原来的基础之上加5分
```
Score.objects.filter(course__teacher__name='黄老师').update(number=F("number")+1)
```
查询两门以上不及格的同学的id、姓名、以及不及格课程数
```
Student.objects.annotate(bad_count=Count("score_number",filter=Q(score_number__lt=60))).filter(bad_count__gte=2).values("id","name","bad_count")
```
查询每门课的选课人数
```
Course.objects.annotate(student_count=Count("score_student")).values("id","name","student_count")
```
