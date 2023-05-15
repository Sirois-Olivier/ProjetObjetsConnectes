using Iot.Core.BLL;
using Iot.Core.DAL;
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
        public ActionResult Index()
        {
            return View();
        }

        public ActionResult About()
        {
            new DALKusto().getData();

            var model = new TableauDeBordModel();

            model.lstHeure = new List<string> { "1", "2", "3" };
            model.lstTemprature = new List<string> { "3", "2", "1" };

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

            return View("Index");
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
    }
}