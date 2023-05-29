using Iot.Core.BLL;
using Iot.Core.DAL;
using Iot.Core.DLL;
using Iot.Mvc.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;

namespace Iot.Mvc.Controllers
{
    public class HomeController : Controller
    {
        public ActionResult Accueil()
        {
            DLLTemperaturePourcentageDate dLLTemperaturePourcentageDate = DALKusto.GetDataTableauDeBord();
            var model = new AccueilModel();

            var temperaturePourcentageDate = dLLTemperaturePourcentageDate.lstTemperaturePourcentageDate[dLLTemperaturePourcentageDate.lstTemperaturePourcentageDate.Count - 1];

            model.pourcentage = temperaturePourcentageDate.pourcentage;
            model.temperature = temperaturePourcentageDate.temperature;

            return View(model);
        }

        public ActionResult TableauDeBord()
        {

            DLLTemperaturePourcentageDate dLLTemperaturePourcentageDate = DALKusto.GetDataTableauDeBord();

            var model = new TableauDeBordModel();

            List<string> lstDateTemp = new List<string>();

            foreach (var date in dLLTemperaturePourcentageDate.lstTemperaturePourcentageDate)
            {
                lstDateTemp.Add(date.date.ToString());
            }

            List<string> lstTemperatureTemp = new List<string>();

            foreach (var temperature in dLLTemperaturePourcentageDate.lstTemperaturePourcentageDate)
            {
                lstTemperatureTemp.Add(Math.Floor(temperature.temperature).ToString());
            }

            model.lstHeure = lstDateTemp;
            model.lstTemprature = lstTemperatureTemp;

            return View(model);
        }

        public ActionResult ModeManuelForm()
        {
            return PartialView("_ModeManuelForm", new ModeManuelFormModel()); 
        }

        [HttpPost]
        public ActionResult SendMessageManualDoor(ModeManuelFormModel model)
        {
            BLLAzureIotManager bLLAzureIotManager = new BLLAzureIotManager();
            bLLAzureIotManager.SendMessageToAzure("Manuel", model.pourcentageOuverture).Wait();

            return View("Accueil");
        }

        [HttpPost]
        public void SendMessageOpenDoor()
        {
            BLLAzureIotManager bLLAzureIotManager = new BLLAzureIotManager();
            bLLAzureIotManager.SendMessageToAzure("Open", "").Wait();
        }

        [HttpPost]
        public void SendMessageCloseDoor()
        {
            BLLAzureIotManager bLLAzureIotManager = new BLLAzureIotManager();
            bLLAzureIotManager.SendMessageToAzure("Close", "").Wait();
        }

        [HttpPost]
        public void SendMessageSetAutomatic()
        {
            BLLAzureIotManager bLLAzureIotManager = new BLLAzureIotManager();
            bLLAzureIotManager.SendMessageToAzure("Automatique", "").Wait();
        }
    }
}