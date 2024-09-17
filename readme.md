## Pinpon oyunun kullanmak isterseniz

udp_camera_server projesini arduino üzerinden Deneyap Karta yüklenmesi gerekiyor. Tek yapılması gereken *udpAddress* kısmının sistem yöneticisinden ağ kısmından bakılması gerekiyor.

Sonrasında Python için bağımılıkların kurulması gerekiyor.

Bunu için projeyi vs code içinde açıp eklentiler kısmında Python ve Python Debug eklentilerinin kurulması gerekiyor

Proje içinde shift+ctrl+p basıp `Python: Create Environment...` yazıp sanal bir ortam oluşturuyoruz. İstenilen isim verilebilir.

Sonrasında PingPong.py dosyası açılıp sağ alttan sanal ortamın seçilmesi gerekiyor.

Sonrasında bağımlılıkları yüklemek için

`pip install -r requirements.txt`

Sonrasında PingPong.py dosyasını çalıştırabilirsiniz