using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Iot.Core.DLL
{
    public class DLLTemperaturePourcentageDate
    {
        public List<DLLTemperaturePourcentageDateItem> lstTemperaturePourcentageDate { get; set; }
    }

    public class DLLTemperaturePourcentageDateItem
    {
        public DateTime date { get; set; }
        public float temperature { get; set; }
        public float pourcentage { get; set; }

    }
}
