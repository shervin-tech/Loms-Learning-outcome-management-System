from rest_framework import serializers
from .models import User  # model.py içinde User sınıfın varsa

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'  # modeldeki tüm alanları serileştirir
