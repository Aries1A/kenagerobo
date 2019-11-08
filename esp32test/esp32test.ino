/*--------------------------------------Client--------------------------------------*/
#include<WiFi.h>
const char *ssid="elecom2g-c08850"; //サーバーのSSID
const char *pass="3A7344CE7169FD2122B9F397AA3EB79F212E5E0741AEF3BB5A5E6BC652F15C0F"; //サーバーのパスワード
//const char *ssid="ist_members"; //サーバーのSSID
//const char *pass="8gAp3nY!s2Gm"; //サーバーのパスワード
static WiFiClient client; //WiFiClient型でclientと宣言
#define TIME 10
#define uS 1000*1000
/*-------------サーバーとWiFi接続-------------*/
bool server_connect()
{
  int try_count = 0;
  WiFi.disconnect();
  WiFi.begin(ssid, pass); //サーバーに接続
  delay(1000);

  while (WiFi.status() != WL_CONNECTED&&try_count<10)
  {
    try_count++;
    Serial.print(".");
    delay(1000);
  }
  if(WiFi.status()==WL_CONNECTED)
  {
    Serial.println("WiFi Connected");
    IPAddress ip(192, 168, 2, 110); //サーバーのIPアドレス
    Serial.println(client.connect(ip, 80)); //IPアドレスとポート番号を指定して接続
    return true;
  }
  else if(try_count == 10)
  {
    Serial.println("WiFi Connection:False");
    WiFi.disconnect();
    delay(100);
    return false;
  }
}
void connect_try()
{
  Serial.println("●WiFi Connnect Start");
  int try_count = 0;
  while(server_connect()!=true&&try_count<5)
  {
    try_count++;
    delay(1000);
  }
  if(try_count==5)
  {
    Serial.println("False");
  }
}
void setup()
{
  Serial.begin(115200);
  Serial.println("Program Start");
  esp_sleep_enable_timer_wakeup(TIME * uS);
  connect_try();
}

void loop()
{
  //サーバーに接続されたか確認
  if(client.connected()==true)
  {
    Serial.println("Massage Send");
    client.println("{\"Name\":\"get_individuals\"}");
    client.stop();
    WiFi.disconnect();
    esp_deep_sleep_start();
  }

}
