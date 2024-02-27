
import django.db.models.deletion

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(

            name='DayName',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128)),
                ('order', models.IntegerField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128)),
                ('description', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('ingredients', models.TextField()),
                ('description', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('preparation_time', models.IntegerField(default=0)),
                ('votes', models.IntegerField(default=0)),
                ('instructions', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='RecipePlan',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('meal_name', models.CharField(max_length=128)),
                ('order', models.IntegerField(unique=True)),
                ('day_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jedzonko.dayname')),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jedzonko.plan')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jedzonko.recipe')),
            ],
        ),
        migrations.AddField(
            model_name='plan',
            name='recipes',
            field=models.ManyToManyField(through='jedzonko.RecipePlan', to='jedzonko.recipe'),
        ),
