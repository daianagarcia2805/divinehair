# Generated by Django 4.1 on 2025-02-18 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cadastros", "0003_perfil_usuario_perfis"),
    ]

    operations = [
        migrations.AlterField(
            model_name="usuario",
            name="perfis",
            field=models.ManyToManyField(
                related_name="usuarios", to="cadastros.perfil"
            ),
        ),
    ]
