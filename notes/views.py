from django.shortcuts import render,redirect

from notes.forms import TaskForm

from notes.models import Task

from django.contrib import messages

from django import forms

# Create your views here.
from django.views.generic import View

from django.db.models import Q

class TaskCreateView(View):

    def get(self,request,*args,**kwargs):

        form_instance=TaskForm()

        return render(request,"task_create.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance=TaskForm(request.POST)

        if form_instance.is_valid():

            form_instance.save()

            # or
            # data=form_instance.cleaned_data

            messages.success(request,"Task is successfully created")

            return redirect("task-list")
        
        else:

            messages.error(request,"Task creation is failed")

            return render(request,"task_create.html",{"form":form_instance})
        

class TaskListView(View):

    def get(self,request,*args,**kwargs):

        search_text=request.GET.get("search_text")

        selected_category=request.GET.get("category","all")

        if selected_category =="all":
            
            qs=Task.objects.all()

        else:
            qs=Task.objects.filter(category=selected_category)

        if search_text!=None:

            qs=Task.objects.filter(Q(title__icontains=search_text)|Q(description__icontains=search_text))

        return render(request,"task_list.html",{"tasks":qs,"selected":selected_category})


class TaskDetailView(View):

    def get(self,request,*args,**kwargs):

        # extract id from url
        id=kwargs.get("pk")

        # fetching task with id
        qs=Task.objects.get(id=id)

        return render(request,"task_detail.html",{"task":qs})

class TaskUpdateView(View):

    def get(self,request,*args,**kwargs):

        # extract pk from kwargs
        id=kwargs.get("pk")

        # fetch task objects with id=id
        task_obj=Task.objects.get(id=id)

        # initialize taskform with task_obj
        form_instance=TaskForm(instance=task_obj)

        # add status field in form_instance
        form_instance.fields["status"]=forms.ChoiceField(choices=Task.status_choices,widget=forms.Select(attrs={"class":"form-control form-select"}),initial=task_obj.status)

        return render(request,"task_edit.html",{"form":form_instance})
    

    def post(self,request,*args,**kwargs):

        # extract id from kwargs
        id=kwargs.get("pk")

        # fetch task object with id
        task_obj=Task.objects.get(id=id)

        # initialize form with request.POST
        form_instance=TaskForm(request.POST,instance=task_obj)

        # check form has errors
        if form_instance.is_valid():

            # add status to form instance
            form_instance.instance.status=request.POST.get("status")

            # save form_instance
            form_instance.save()

            # redirect to task list
            return redirect("task-list")
        
        else:

            return render(request,"task_edit.html",{"form":form_instance})


class TaskDeleteView(View):

    def get(self,request,*args,**kwargs):

        # extract id amd delete task object with this id
        Task.objects.get(id=kwargs.get("pk")).delete()

        return redirect("task-list")
    

from django.db.models import Count
    
class TaskSummaryView(View):

    def get(self,request,*args,**kwargs):

        qs=Task.objects.all()

        total_task_count=qs.count()

        category_summary=Task.objects.all().values("category").annotate(cat_count=Count("category"))
        print(category_summary)

        status_summary=Task.objects.all().values("status").annotate(status_count=Count("status"))
        print(status_summary)



        context={
            "total_task_count":total_task_count,
            "category_summary":category_summary,
            "status_summary":status_summary,

        }

        return render(request,"task_summary.html",context)

