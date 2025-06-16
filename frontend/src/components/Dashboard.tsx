import * as React from 'react';
import { useEffect, useState } from 'react';
import type { FC } from 'react';
import { Grid, Paper, Typography, CircularProgress, Box } from '@mui/material';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import axios from 'axios';

interface AnalysisData {
  postgres: {
    topCustomers: Array<{ customer_id: number; total_value: number }>;
    categoryAnalysis: Array<{ category: string; total_sales: number }>;
    monthlyTrend: Array<{ month: string; total_sales: number }>;
  };
  mongodb: {
    mostViewedProducts: Array<{ product_id: number; views: number }>;
    userSessionAnalysis: {
      avgEventsPerSession: number;
      avgUniquePagesPerSession: number;
      purchaseConversionRate: number;
    };
    hourlyTraffic: Array<{
      hour: string;
      add_to_cart: number;
      cart_view: number;
      checkout: number;
      page_view: number;
      purchase: number;
      remove_from_cart: number;
    }>;
  };
}

const Dashboard: FC = () => {
  const [data, setData] = useState<AnalysisData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('http://localhost:5001/api/analysis');
        setData(response.data);
        setLoading(false);
      } catch (err) {
        setError('Failed to fetch analysis data');
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Typography color="error" align="center">
        {error}
      </Typography>
    );
  }

  if (!data) {
    return null;
  }

  return (
    <Grid container spacing={3}>
      {/* PostgreSQL Analysis */}
      <Grid item xs={12}>
        <Typography variant="h5" gutterBottom>
          PostgreSQL Analysis
        </Typography>
      </Grid>

      {/* Top Customers */}
      <Grid item xs={12} md={6}>
        <Paper sx={{ p: 2 }}>
          <Typography variant="h6" gutterBottom>
            Top 5 Customers by Total Order Value
          </Typography>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={data.postgres.topCustomers}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="customer_id" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="total_value" fill="#8884d8" name="Total Value" />
            </BarChart>
          </ResponsiveContainer>
        </Paper>
      </Grid>

      {/* Category Analysis */}
      <Grid item xs={12} md={6}>
        <Paper sx={{ p: 2 }}>
          <Typography variant="h6" gutterBottom>
            Product Category Analysis
          </Typography>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={data.postgres.categoryAnalysis}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="category" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="total_sales" fill="#82ca9d" name="Total Sales" />
            </BarChart>
          </ResponsiveContainer>
        </Paper>
      </Grid>

      {/* MongoDB Analysis */}
      <Grid item xs={12}>
        <Typography variant="h5" gutterBottom sx={{ mt: 4 }}>
          MongoDB Analysis
        </Typography>
      </Grid>

      {/* Most Viewed Products */}
      <Grid item xs={12} md={6}>
        <Paper sx={{ p: 2 }}>
          <Typography variant="h6" gutterBottom>
            Most Viewed Products
          </Typography>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={data.mongodb.mostViewedProducts}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="product_id" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="views" fill="#ffc658" name="Views" />
            </BarChart>
          </ResponsiveContainer>
        </Paper>
      </Grid>

      {/* User Session Analysis */}
      <Grid item xs={12} md={6}>
        <Paper sx={{ p: 2 }}>
          <Typography variant="h6" gutterBottom>
            User Session Analysis
          </Typography>
          <Typography>
            Average Events per Session: {data.mongodb.userSessionAnalysis.avgEventsPerSession.toFixed(2)}
          </Typography>
          <Typography>
            Average Unique Pages per Session: {data.mongodb.userSessionAnalysis.avgUniquePagesPerSession.toFixed(2)}
          </Typography>
          <Typography>
            Purchase Conversion Rate: {data.mongodb.userSessionAnalysis.purchaseConversionRate.toFixed(2)}%
          </Typography>
        </Paper>
      </Grid>

      {/* Hourly Traffic Analysis */}
      <Grid item xs={12}>
        <Paper sx={{ p: 2 }}>
          <Typography variant="h6" gutterBottom>
            Hourly Traffic Analysis
          </Typography>
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={data.mongodb.hourlyTraffic}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="hour" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="page_view" fill="#8884d8" name="Page Views" />
              <Bar dataKey="add_to_cart" fill="#82ca9d" name="Add to Cart" />
              <Bar dataKey="cart_view" fill="#ffc658" name="Cart Views" />
              <Bar dataKey="checkout" fill="#ff8042" name="Checkout" />
              <Bar dataKey="purchase" fill="#0088fe" name="Purchase" />
              <Bar dataKey="remove_from_cart" fill="#ff0000" name="Remove from Cart" />
            </BarChart>
          </ResponsiveContainer>
        </Paper>
      </Grid>
    </Grid>
  );
};

export default Dashboard; 