function calcBMI() {
    var weight = document.bmiform.pounds.value, height = document.bmiform.inches.value;
    document.bmiform.bmi.value = parseFloat((weight) / ((height/100) * (height/100)));
  }
  
  function myfun()
  {
    bmi = document.getElementById("bmi").value;
    gender = document.getElementById("gender").value;
    document.getElementById("gender-info").innerText = gender;
    var dietplan ="";
    var calo = 0
    var pro = "" 
    var carbo = ""
    var fat = ""
    var calci = ""

    if(gender == "male" || gender == "Male")
    {
        if(bmi < 18.5)
        {
            // document.getElementById("table1");
            // toggleTable1();
            // return false;
            dietplan = "Nutrition Diet Plan for Weight Gain"
            calo = 2800
            pro = "55-60g"
            carbo = "240-300g"
            fat = "40-100g"
            calci = "450g"

        }
        if(bmi > 18.5 && bmi < 22.9)
        {
            // document.getElementById("table2");
            // toggleTable2();
            // return false;
            dietplan = "Nutrition Diet Plan for Normal Weight"
            calo = 2400
            pro = "55g"
            carbo = "240-300g"
            fat = "40-80g"
            calci = "420g"
        }
        if(bmi > 22.9)
        {
            // document.getElementById("table3");
            // toggleTable3();
            // return false;
            dietplan = "Nutrition Diet Plan for Weight Loss"
            calo = 1800
            pro = "30-130g"
            carbo = "200-240g"
            fat = "30-70g"
            calci = "450mg"
        }
    }
    if(gender == "female" || gender == "Female")
    {
        if(bmi < 18.5)
        {
            // document.getElementById("table4");
            // toggleTable4();
            // return false;
            dietplan = "Nutrition Diet Plan for Weight Gain"
            calo = 2200
            pro = "45-55g"
            carbo = "200-280g"
            fat = "50-80g"
            calci = "450g"
        }
        if(bmi > 18.5 && bmi < 22.9)
        {
            // document.getElementById("table5");
            // toggleTable5();
            // return false;
            dietplan = "Nutrition Diet Plan for Normal Weight"
            calo = 2200
            pro = "45g"
            carbo = "200-280g"
            fat = "50-80g"
            calci = "420g"
        }
        if(bmi > 22.9)
        {
            // document.getElementById("table6");
            // toggleTable6();
            // return false;
            dietplan = "Nutrition Diet Plan for Weight Loss"
            calo = 1500
            pro = "60-120g"
            carbo = "180-220g"
            fat = "25-50g"
            calci = "450g"
        }
    }
    document.getElementById("myTable1").style.display ='block';
    document.getElementById('weight-info').innerText = dietplan;
    document.getElementById('calories').innerText = calo;
    document.getElementById('protein').innerText = pro;
    document.getElementById('carbohydrates').innerText = carbo;
    document.getElementById('fat').innerText = fat;
    document.getElementById('calcium').innerText = calci;
    console.log(dietplan);
    // document.getElementById("myTable1").classList.toggle("hidden");
  }
  
  function toggleTable1() {
    document.getElementById("myTable1").classList.toggle("hidden");
  }


//   function toggleTable2() {
//     document.getElementById("myTable2").classList.toggle("hidden");
//   }
//   function toggleTable3() {
//     document.getElementById("myTable3").classList.toggle("hidden");
//   }
//   function toggleTable4() {
//     document.getElementById("myTable4").classList.toggle("hidden");
//   }
//   function toggleTable5() {
//     document.getElementById("myTable5").classList.toggle("hidden");
//   }
//   function toggleTable6() {
//     document.getElementById("myTable6").classList.toggle("hidden");
//   }