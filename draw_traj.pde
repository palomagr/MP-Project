//import org.joda.time.DateTime;
//import org.joda.time.Duration;
//import org.joda.time.Interval;
//import org.joda.time.format.DateTimeFormat;

BufferedReader reader;
String line;
String[] pieces;
int usercolor0 = -2000;
int usercolor1 = -1800;
int usercolor2 = -10000;
int user = 100;
//int index = 0;
//ArrayList <DateTime> time = new ArrayList();
//ArrayList <String> timeS = new ArrayList();
String file = "test.txt";
ArrayList<PVector> points0 = new ArrayList();
ArrayList<PVector> points1 = new ArrayList();
ArrayList<PVector> points2 = new ArrayList();
PVector a;
PVector b;
 

void setup() 
{
  size(900, 900);
  reader = createReader(file);   
  strokeWeight(1);
  background(0);
  image(loadImage("machu.jpg"),0,0);
}

void draw() 
{  
  try { line = reader.readLine(); } 
  
  catch (IOException e) {
    e.printStackTrace();
    line = null; }
    
  if (line != null) {
    pieces = split(line, "\t");  
    user = int(pieces[0]);

    if (user == 0) {
      float x = (float(pieces[1]))+10;                
      float y = (float(pieces[2]))+15;
      points0.add(new PVector(x,y)); } 
      
    else if (user == 1) {
      float x = (float(pieces[1]))+10;                
      float y = (float(pieces[2]))+15;
      points1.add(new PVector(x,y)); } 
      
    else if (user == 2) {
      float x = (float(pieces[1]))+10;                
      float y = (float(pieces[2]))+15;
      points2.add(new PVector(x,y)); } 
  
  if (points0.size() > 1) {  
    stroke(usercolor0);
    for (int i = points0.size()-1; i<points0.size(); i++) {
      strokeWeight(7);
      a = points0.get(i-1);
      b = points0.get(i);
      point(b.x,b.y); 
      strokeWeight(1);
      line(a.x,a.y,b.x,b.y); }
    }
      
  if (points1.size() > 1) {  
    stroke(usercolor1);
    for (int i = points1.size()-1; i<points1.size(); i++) {
      strokeWeight(7);
      a = points1.get(i-1);
      b = points1.get(i);
      point(b.x,b.y); 
      strokeWeight(1);
      line(a.x,a.y,b.x,b.y); }
    }
    
  if (points2.size() > 1) {  
    stroke(usercolor2);
    for (int i = points2.size()-1; i<points2.size(); i++) {
      strokeWeight(7);
      a = points2.get(i-1);
      b = points2.get(i);
      point(b.x,b.y); 
      strokeWeight(1);
      line(a.x,a.y,b.x,b.y); }
    }
  }

  else {
    saveFrame();
    noLoop();    
    print("done");
    exit(); }
}

//    fill(0);
//    noStroke();
//    rect(0,0,90,30);
//    fill(255);
//    textSize(20);
//    text("user: " + (index), 10,23);

void keyPressed() {
  if (key == 'e') {
    println("e pressed");
    saveFrame();
    endRecord();
    exit();
  }
}
