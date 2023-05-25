using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Iot.Core.DLL
{
    public class DLLTemperatureDate
    {
        public List<DLLTemperatureDateItem> lstTemperatureDate { get; set; }
    }

    public class DLLTemperatureDateItem
    {
        public DateTime date { get; set; }
        public float temperature { get; set; }
    }
}
