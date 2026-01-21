from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib import messages
from apps.users.models import User
from apps.users.forms import UserForm


class UserCreateView(CreateView):
    model = User
    form_class = UserForm
    success_url = "/usuarios/listar/"
    def form_valid(self, form):
        messages.success(self.request, 'Usuário criado com sucesso!')
        return super().form_valid(form)
    
class UserListView(ListView):
    model = User
    context_object_name = "users"
    paginate_by = 10
    
class UserUpdateView(UpdateView):
    model = User
    form_class = UserForm
    success_url = "/usuarios/listar/"
    def form_valid(self, form):
        messages.success(self.request, 'Usuário atualizado com sucesso!')
        return super().form_valid(form)    
        
class UserDeleteView(DeleteView):
    model = User
    success_url = "/usuarios/listar/"