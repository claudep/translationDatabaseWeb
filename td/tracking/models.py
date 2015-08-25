from django.db import models

from django.utils import timezone


# Choices
LANG_NAMES = (
	('indonesian', 'Bahasa Indonesia'),
	('english', 'English (American)'),
	('british', 'English (British)'),
	('german', 'German'),
)

LANG_TAGS = (
	('ina', 'ina'),
	('eng', 'eng'),
	('bri', 'bri'),
	('deu', 'deu'),
)

OUTPUT_TARGETS = (
	('print', 'print'),
	('audio', 'audio'),
	('other', 'other'),
)

TRANSLATION_METHODS = (
	('lit', 'literal'),
	('dyn', 'dynamic'),
	('other', 'other'),
)

TECHNOLOGIES = (
	('btak', 'btak'),
	('tk', 'trasnlation keyboard'),
	('other', 'other'),
)

# Models
class Charter(models.Model):

	# name should be made the same as the target language 
	name = models.CharField(
		max_length = 100,
		unique = True,
	)
	number = models.CharField(
		max_length = 50,
		unique = True,
		blank = True,
	)

	# target_lang_name and target_lang_ietf should be pre-populated
	target_lang_ietf = models.CharField(
		max_length = 200,
		primary_key = True,
		choices = LANG_TAGS,
	)
	# target_lang name will be automatically selected based on target_lang_ietf
	target_lang_name = models.CharField(
		max_length = 100,
		choices = LANG_NAMES,
	)

	# gw_lang_ietf and gw_lang_name should be automatically filled based on the target_lang_ietf
	gw_lang_ietf = models.SlugField(
		choices = LANG_TAGS,
	)
	gw_lang_name = models.CharField(
		max_length = 100,
		choices = LANG_NAMES,
	)

	start_date = models.DateField(
		# default = now
	)
	end_date = models.DateField(
		blank = True,
	)

	lead_dept = models.CharField(
		max_length = 200,
		blank = True,
	)

	# Relationship field
	countries = models.ManyToManyField(
		'Country',
		blank = True,
	)

	# 
	created_at = models.DateTimeField(
		default = timezone.now
	)

	created_by = models.CharField(
		max_length = 200
	)

	def __unicode__(self):
		return self.target_lang_name

	def get_fields(self):
		return [(field.name, field.value_to_string(self)) for field in Charter._meta.fields]


class Event(models.Model):

	# Primary key is default

	charter = models.ForeignKey(Charter)

	location = models.CharField(
		max_length = 200,
		blank = True,
	)

	start_date = models.DateField(
	)
	end_date = models.DateField(
		blank = True,
	)

	lead_dept = models.CharField(
		max_length = 200,
		blank = True,
	)

	output_target = models.SlugField(
		choices = OUTPUT_TARGETS,
		blank = True,
	)

	translation_method = models.SlugField(
		choices = TRANSLATION_METHODS,
		blank = True,
	)

	tech_used = models.SlugField(
		choices = TECHNOLOGIES,
		blank = True,
	)
	comp_tech_used = models.SlugField(
		choices = TECHNOLOGIES,
		blank = True,
	)

	pub_process = models.TextField(
		max_length = 1500,
		blank = True,
	)

	follow_up = models.CharField(
		max_length = 200,
		blank = True,
	)

	# Relationship fields
	materials    = models.ManyToManyField('Material')
	translators  = models.ManyToManyField('Translator')
	facilitators = models.ManyToManyField('Facilitator')
	networks     = models.ManyToManyField('Network')
	departments  = models.ManyToManyField('Department')

	# Functions
	def __unicode__(self):
		return str(self.id)
	def get_fields(self):
		return [(field.name, field.value_to_string(self)) for field in Event._meta.fields]


class Material(models.Model):

	name = models.CharField(
		max_length = 200
	)

	licensed = models.BooleanField(
		default = False
	)


class Translator(models.Model):

	name = models.CharField(
		max_length = 200
	)


class Facilitator(models.Model):

	name = models.CharField(
		max_length = 200
	)

	is_lead = models.BooleanField(
		default = False
	)

	speaks_gl = models.BooleanField(
		default = False
	)


class Network(models.Model):

	name = models.CharField(
		max_length = 200
	)


class Department(models.Model):

	name = models.CharField(
		max_length = 200
	)


# Dummy models
class Country(models.Model):

	name = models.CharField(max_length=200)


class Language(models.Model):

	name = models.CharField(max_length=200)
	ietf = models.SlugField()