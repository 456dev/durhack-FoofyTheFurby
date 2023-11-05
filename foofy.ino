#define enCLK 4
#define enDT 5
#define reSW 3
#define rEY 10
#define lEY 11
#define home 2

boolean freeze=true;

int targetposition;
int currentStateCLK;
int previousStateCLK;
int position;

long count;
int maxcount = 750;
long yapcount = 0;

String code="";
String lastcode="";
String incomingByte;

int homecount=0;

void setup() {
   pinMode (enCLK,INPUT);
   pinMode (enDT,INPUT);  
   pinMode (reSW,OUTPUT);
   pinMode (rEY,OUTPUT);
   pinMode (lEY,OUTPUT);
   pinMode (home,INPUT_PULLUP);
   Serial.begin(9600);
   //Serial.setTimeout(1); 
   previousStateCLK = digitalRead(enCLK);
   code = "home";
   //code home: reset motor to home
}

void loop() {
  //check for sent commands
  if (Serial.available()>0){
    incomingByte = Serial.readStringUntil('\n');
    //Serial.print("I received: ");
    Serial.println(incomingByte);
    Serial.println(lastcode);
    Serial.println(code);
    if (lastcode=="" && code==""){
      code=incomingByte;
    }
    if (code=="speak" && incomingByte=="nospeak") {
      code="home";
    }
  }//clear
  
  currentStateCLK = digitalRead(enCLK);
  if (currentStateCLK != previousStateCLK){
     // If the inputDT state is different than the inputCLK state then
     // the encoder is rotating counterclockwise
     if (digitalRead(enDT) != currentStateCLK) {
       position--;
       //Serial.print(" -- Value: ");
       //Serial.println(position);
     } else {
       // Encoder is rotating clockwise
       position++;
       //Serial.print(" -- Value: ");
       //Serial.println(position);    
     }
     //Serial.print(" -- Value: ");
     //Serial.println(position);
   }
   // Update previousStateCLK with the current state
   previousStateCLK = currentStateCLK;
  //clear

  if (code=="speak"){
    delay(random(50,1000));
    if (digitalRead(reSW)==HIGH){
      digitalWrite(reSW, LOW);
    }else{
      digitalWrite(reSW, HIGH);
    }
  }

  if (code=="nospeak"){
    
  }

  if (code=="reset"){//reset code
    Serial.println("reset called");
    setup();
  }//clear
  
  if (code=="sleep"){//sleep code
    Serial.println("sleep called");
    code="";
    lastcode="";
    digitalWrite(rEY, LOW);
    digitalWrite(lEY, LOW);
    digitalWrite(reSW,HIGH);
    freeze=false;
    delay(1000);
    freeze=true;
    Serial.println("sleep return");
  }
 
  if (code=="wake"){//sleep code
    Serial.println("wake called");
    code="";
    lastcode="";
    digitalWrite(rEY, HIGH);
    digitalWrite(lEY, HIGH);
    digitalWrite(reSW,LOW);
    freeze=false;
    delay(1000);
    freeze=true;
    Serial.println("wake return");
  }

   if (code=="boogie"){
    Serial.println("boogie called");
    freeze==false;
    code="";
    lastcode="";    
   }

  //set to home code
  if (code=="home"){
    Serial.println("home called");
    freeze=false;
    if (digitalRead(home)==LOW){
      freeze="true";
      code="";
      lastcode="home";
    }
    if (lastcode=="home"){
      if (digitalRead(home)==HIGH){
        code="home";
      }else{
        lastcode="";
        digitalWrite(rEY, HIGH);
        digitalWrite(lEY, HIGH);
        //position=0;
        //currentStateCLK=0;
        previousStateCLK=0;
        //Serial.println(position);  
        Serial.println("home return");  
      }
    }
  }//clear


  //cycle count for freeze jitter
  count=count+1;
  if (count==maxcount && freeze){
    count=0;
    if (digitalRead(reSW)==LOW){
      pinMode (reSW,OUTPUT);
      digitalWrite(reSW, HIGH);
    }else{
      digitalWrite(reSW, LOW);
    }
  }
}
