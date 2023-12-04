# SeuApp/forms.py
from django import forms
from django.contrib.auth.forms import SetPasswordForm
from django.utils.translation import gettext as _

class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Ajuste as mensagens conforme necessário
        self.fields['new_password1'].help_text = _(
            "A senha deve ter pelo menos 8 caracteres e não pode ser muito parecida com as informações pessoais."
        )
        self.fields['new_password2'].help_text = _("Digite a nova senha novamente para confirmação.")

    class Meta:
        model = User  # Substitua pelo seu modelo de usuário, se diferente do padrão
