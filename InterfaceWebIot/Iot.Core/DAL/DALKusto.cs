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
    public static class DALKusto
    {
        static KustoConnectionStringBuilder builder = new KustoConnectionStringBuilder("https://clusterserre.eastus2.kusto.windows.net/databaseserre").WithAadUserPromptAuthentication();

        public static void GetData()
        { 
            var client = Kusto.Data.Net.Client.KustoClientFactory.CreateCslQueryProvider(builder);
            var reader = client.ExecuteQuery("tableserre | count");

            reader.Close();

        }  
    }
}
