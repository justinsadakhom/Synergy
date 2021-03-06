from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models import BooleanField, URLField
from django.utils.translation import ugettext_lazy as _


# Custom validators

def validate_name(name: str):

    if len(name) < 2:
        raise ValidationError('Name must have at least 2 characters')

    for char in name:
        if not (char.isalpha() or char.isnumeric() or char == ' '):
            raise ValidationError('Name cannot have special characters')


# Database models

class Business(models.Model):
    """ An abstract class representing a business using the website.

    Attributes:
        name (str): Title of the business.
        country (str): Where the business is located.
        industry (str): The primary industry of the business.
        postal_code (str): The business's postal code.
        website (str): The business's website.
    """

    # Choices

    CAN = 'CAN'
    USA = 'USA'
    OTH = 'OTH'

    COUNTRY_CHOICES = [
        (None, '- Select -'),
        (CAN, 'Canada'),
        (USA, 'United States'),
        (OTH, 'Other')
    ]

    AERO = 'AERO'
    AGRI = 'AGRI'
    AUTO = 'AUTO'
    BUSI = 'BUSI'
    CHEM = 'CHEM'
    CONS = 'CONS'
    DIST = 'DIST'
    EDUC = 'EDUC'
    ELCE = 'ELCE'
    ELCT = 'ELCT'
    ENGI = 'ENGI'
    FOOD = 'FOOD'
    GOVE = 'GOVE'
    MACH = 'MACH'
    MANU = 'MANU'
    MEDI = 'MEDI'
    META = 'META'
    MINI = 'MINI'
    PAPE = 'PAPE'
    PLAS = 'PLAS'
    TEXT = 'TEXT'
    TRAN = 'TRAN'
    UTIL = 'UTIL'

    INDUSTRY_CHOICES = [
        (None, '- Select -'),
        (AERO, 'Aerospace & Defense'),
        (AGRI, 'Agriculture & Forestry'),
        (AUTO, 'Automotive'),
        (BUSI, 'Business'),
        (CHEM, 'Chemicals'),
        (CONS, 'Construction'),
        (DIST, 'Distribution, Wholesale, Retail'),
        (EDUC, 'Education'),
        (ELCE, 'Electrical Equipment'),
        (ELCT, 'Electronics'),
        (ENGI, 'Engineering & Technical Services'),
        (FOOD, 'Food, Beverage, Tobacco'),
        (GOVE, 'Government & Military'),
        (MACH, 'Machinery'),
        (MANU, 'Manufacturing'),
        (MEDI, 'Medical & Healthcare'),
        (META, 'Metals - Raw, Formed, Fabricated'),
        (MINI, 'Mining, Oil & Gas, Quarrying'),
        (OTH, 'Other'),
        (PAPE, 'Paper, Paper Products, Printing'),
        (PLAS, 'Plastics & Rubber'),
        (TEXT, 'Textiles, Apparel, Leather'),
        (TRAN, 'Transportation & Logistics'),
        (UTIL, 'Utilities & Telecommunications')
    ]

    # Fields

    name = models.CharField(max_length=30)

    country = models.CharField(
        max_length=3,
        choices=COUNTRY_CHOICES
    )

    industry = models.CharField(
        max_length=4,
        choices=INDUSTRY_CHOICES
    )

    postal_code = models.CharField(
        max_length=7,
        null=True
    )

    website = URLField(
        null=True
    )

    class Meta:
        verbose_name_plural = "businesses"

    def __str__(self):
        return self.name


class Product(models.Model):
    """ A commodity available for purchase.

    Attributes:
        name (str): Name of the product.
        quantity (int): How much is available for a single order.
        cost (float): Cost per unit, in dollars.
        supplier (Supplier): The business supplying the product.
        _quality (float): Quality rating, from a scale of 0.0 to 5.0.
    """

    name = models.CharField(max_length=30, validators=[validate_name])
    quantity = models.IntegerField(validators=[MinValueValidator(0)])

    cost = models.DecimalField(
        decimal_places=2,
        max_digits=6,
        validators=[MinValueValidator(0.0)]
    )

    _quality = models.DecimalField(
        default=0.0,
        max_digits=2,
        decimal_places=1,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        db_column='quality'
    )

    def __str__(self):

        name = str(self.name).capitalize()

        return '{0} – Price: ${1}, In Stock: {2}' \
            .format(name, self.cost, self.quantity)


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""

        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""

        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):

    def __init__(self, *args, **kwargs):
        super(AbstractUser, self).__init__(*args, **kwargs)

    # Choices

    END = 'END'
    SPL = 'SPL'
    MOP = 'MOP'
    GEN = 'GEN'
    SAM = 'SAM'
    OTH = 'OTH'

    JOB_FUNCTION_CHOICES = [
        (None, '- Select -'),
        (END, 'Engineering / Design'),
        (SPL, 'Supply Chain / Procurement / Logistics'),
        (MOP, 'Manufacturing / Operations'),
        (GEN, 'General Management'),
        (SAM, 'Sales & Marketing'),
        (OTH, 'Other')
    ]

    # Fields

    job_title = models.CharField(
        max_length=30,
        null=True
    )

    job_function = models.CharField(
        max_length=3,
        choices=JOB_FUNCTION_CHOICES,
        null=True
    )

    company = models.ForeignKey(
        'Business',
        on_delete=models.CASCADE,
        null=True
    )

    info_complete = BooleanField(default=False)
    verified = BooleanField(default=False)

    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()  # Specify custom Manager

    def __str__(self):
        return self.first_name
