from django.db import models
from common.models import AuditModel


SIDE_CHOICES = [
    ('maternal', 'Maternal'),
    ('paternal', 'Paternal'),
    ('unknown', 'Unknown'),
]


class Person(AuditModel):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    death_date = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    def __str__(self):
        return f"{self.first_name} {self.last_name or ''}".strip()


class Relation(AuditModel):
    RELATION_TYPES = [
        ('father', 'Father'),
        ('mother', 'Mother'),
        ('child', 'Child'),
        ('spouse', 'Spouse'),
        ('sibling', 'Sibling'),
        ('aunt', 'Aunt'),
        ('uncle', 'Uncle'),
        ('grandparent', 'Grandparent'),
    ]


    from_person = models.ForeignKey(Person, related_name='relations_from', on_delete=models.CASCADE)
    to_person = models.ForeignKey(Person, related_name='relations_to', on_delete=models.CASCADE)
    relation_type = models.CharField(max_length=15, choices=RELATION_TYPES)
    side = models.CharField(max_length=10, choices=SIDE_CHOICES, default='unknown', blank=True, null=True)

    class Meta:
        unique_together = ('from_person', 'to_person', 'relation_type', 'side')

    def __str__(self):
        side_str = f" ({self.side})" if self.side and self.side != 'unknown' else ""
        return f"{self.from_person} is {self.side} {self.relation_type} of {self.to_person}{side_str}"


class RelationStatus(AuditModel):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('divorced', 'Divorced'),
        ('separated', 'Separated'),
        ('broken', 'Broken'),
        ('complicated', 'Complicated'),
        ('widowed', 'Widowed'),
    ]

    relation = models.ForeignKey('Relation', related_name='statuses', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.relation} - {self.status} ({self.start_date} - {self.end_date or 'Present'})"
