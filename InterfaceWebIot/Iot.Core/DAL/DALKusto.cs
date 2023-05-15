using Kusto.Data.Common;
using Kusto.Data.Net.Client;
using Kusto.Data;
using System;
using System.Collections.Generic;
using System.Diagnostics.Metrics;
using System.Linq;
using System.Security.Policy;
using System.Text;
using System.Threading.Tasks;

namespace Iot.Core.DAL
{
    public class DALKusto
    {
        public void getData()
        {
            var client = Kusto.Data.Net.Client.KustoClientFactory.CreateCslQueryProvider("https://clusterserre.eastus2.kusto.windows.net/databaseserre;Fed=true");
            var reader = client.ExecuteQuery("tableserre | count");

            reader.Close();
              
        }  
    }
}
