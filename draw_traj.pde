import org.joda.time.DateTime;
import org.joda.time.Duration;
import org.joda.time.Interval;
import org.joda.time.format.DateTimeFormat;


BufferedReader reader;
String line;
int usercolor0;
int usercolor1;
int usercolor2;
int index;
String usernum;
PImage img;
ArrayList <DateTime> time = new ArrayList();
ArrayList <String> timeS = new ArrayList();
float millis=0.0;
String user_string;
String file_out;
String user_num = "";
String rn = "charm";
String file = "dj02_2.txt";
ArrayList<PVector> points0 = new ArrayList();
ArrayList<PVector> points1 = new ArrayList();
ArrayList<PVector> points2 = new ArrayList();
 

void setup() 
{
  size(900, 900);
  reader = createReader(file);
  file_out = rn + "_" + user_num + "_subject_";    
  strokeWeight(1);
  
  usernum = " 0 ";
  index = 0;
  img = loadImage("machu.jpg");
  background(0);
  image(img,0,0);
  delay(3000);
}

void draw() 
{  
  try { line = reader.readLine(); } 
  
  catch (IOException e) {
    e.printStackTrace();
    line = null; }
  
  if (line == null) {
    saveFrame();
    noLoop();    
    print("done");
    exit(); }
  
  else {
    String[] pieces = split(line, "\t");  
    String user = pieces[0];
    user_string = pieces[0]; 
    usercolor0 = -2000;
    usercolor1 = -1800;
    usercolor2 = -1600;

    if (int(user) == 0) {
      float x = (abs(float(pieces[1])))*.98;                
      float y = (abs(float(pieces[2])))*.918;
      PVector p = new PVector(x,y);
      points0.add(p); } 
      
//    else if (int(user) == 1) {
//      float x = (abs(float(pieces[1])))*.98;                
//      float y = (abs(float(pieces[2])))*.918;
//      PVector p = new PVector(x,y);
//      points1.add(p); } 
      
    else if (int(user) == 2) {
      float x = (abs(float(pieces[1])))*.98;                
      float y = (abs(float(pieces[2])))*.918;
      PVector p = new PVector(x,y);
      points2.add(p); } 
    
  }

//    fill(0);
//    noStroke();
//    rect(0,0,90,30);
//    fill(255);
//    textSize(20);
//    text("user: " + (index), 10,23);
    
  for (int i=1;i<points0.size();i++) {
    stroke(usercolor0);
    strokeWeight(7);
    PVector a = points0.get(i-1);
    PVector b = points0.get(i);
    point(a.x,a.y);
    strokeWeight(1);
    line(a.x,a.y,b.x,b.y); }
    
  for (int i=1;i<points1.size();i++) {
    stroke(usercolor1);
    strokeWeight(7);
    PVector a = points1.get(i-1);
    PVector b = points1.get(i);
    point(a.x,a.y);
    strokeWeight(1);
    line(a.x,a.y,b.x,b.y); }
 
}



void keyPressed() {
  if (key == 'e') {
    saveFrame();
    endRecord();
    exit();
  }
}
