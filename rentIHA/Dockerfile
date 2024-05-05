# docker-compose up --build işleminden sonra superuser oluşturup devamında gerekli gruplar oluşturulup (user_group,admin_group) yetkileri verildikten sonra sistem kullanılmaya hazırdır!

# Base image
FROM python:3.12.3

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# çalışma alanını set et
WORKDIR /code

# Bağımlılıkların dosyasını kopyala ve yükle
COPY requirements.txt /code/
# Gerekli python kodlarını çalıştırmak için bir script dosyası kopyala
COPY python_command.sh /code/
# Sh dosyasını çalıştırılabilri hale getirdim
RUN chmod +x /code/python_command.sh
# bağımlılıkları indir
RUN pip install --no-cache-dir -r requirements.txt

# proje dosyalarını kopyala
COPY . /code/
