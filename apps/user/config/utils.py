from datetime import datetime
import os
from django.core.exceptions import ValidationError


def profile_image_storage(instance, filename):
    profile_id = instance.id

    if profile_id is None:
        profile_id = "new"

    ext = filename.split('.')[-1]
    current_date = datetime.now().strftime('%d-%m-%Y')
    new_filename = f'profile_{profile_id}_image_{current_date}.{ext}'

    return os.path.join('profile_images/', new_filename)

def validate_image_extension(image):
    allowed_extensions = ['jpeg', 'jpg', 'png', 'gif']
    extension = image.name.split('.')[-1].lower()

    if extension not in allowed_extensions:
        raise ValidationError(
            'Invalid image format. Please upload a valid image file (JPG, JPEG, PNG, GIF).'
        )

def validate_max_file_size(value):
    max_size_byte = 5242880  # 5MB
    max_size_mb = max_size_byte / (1024**2)

    if value.size > max_size_byte:
        raise ValidationError(f'File size cannot exceed {max_size_mb} MB.')
