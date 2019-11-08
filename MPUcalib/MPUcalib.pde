void setup() {
  size(500, 500, P3D); //P3Dライブラリを使う
  background(0);
  noFill();
  stroke(255);  
}

void draw() {
  background(0);

  translate(width/2, height/2);
  rotateY(frameCount / 200.0);

  box(300);
}
