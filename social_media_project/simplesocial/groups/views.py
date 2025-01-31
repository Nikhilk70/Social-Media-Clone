from django.shortcuts import render
from django.contrib import messages
from django.db import IntegrityError
from . import models
from django.http import Http404
from django.shortcuts import get_object_or_404


# Create your views here.
from django.contrib.auth.mixins import (LoginRequiredMixin,PermissionRequiredMixin)


from django.urls import reverse
from django.views import generic

from groups.models import Group, GroupMember

class CreateGroup(LoginRequiredMixin,generic.CreateView):
    fields = ('name','description')
    model = Group
    
class SingleGroup(generic.DetailView):
    model = Group
    
class ListGroups(generic.ListView):
    model = Group
    
class JoinGroup(LoginRequiredMixin, generic.RedirectView):
    
    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:single', kwargs={'slug': self.kwargs.get('slug')})
    
    def get(self, request, *args, **kwargs):
        group = get_object_or_404(Group, slug=self.kwargs.get('slug'))
        
        try:
            GroupMember.objects.create(user=self.request.user, group=group)
            messages.success(self.request, 'You are now a member!')
        except IntegrityError:  # Raised if the user is already a member
            messages.warning(self.request, 'You are already a member of this group!')
        
        return super().get(request, *args, **kwargs)
            
class LeaveGroup(LoginRequiredMixin, generic.RedirectView):
    
    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:single', kwargs={'slug': self.kwargs.get('slug')})
    
    def get(self, request, *args, **kwargs):
        group = get_object_or_404(Group, slug=self.kwargs.get('slug'))
        
        try:
            membership = GroupMember.objects.get(user=self.request.user, group=group)
            membership.delete()
            messages.success(self.request, 'You have left the group.')
        except GroupMember.DoesNotExist:
            messages.warning(self.request, 'You are not a member of this group.')
        
        return super().get(request, *args, **kwargs)
