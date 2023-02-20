/** @odoo-module **/

import { Component, onWillStart, onMounted, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { loadJS } from "@web/core/assets";

class PoultryDashboard extends Component {
    setup() {
        this.orm = useService("orm");

        this.state = useState({
            total_birds: 0,
            death_count: 0,
            mortality_rate: 0,

            feed_stock: 0,
            purchase_total: 0,
            sale_total: 0,
            cash_balance: 0,

            selected_year: "all",
        });

        this.deathChart = null;
        this.profitChart = null;

        onWillStart(async () => {
            await loadJS("https://cdn.jsdelivr.net/npm/chart.js");
            await this.loadData();
        });

        onMounted(() => {
            this.renderCharts();
        });
    }

    // ================= LOAD DATA =================
    async loadData() {

        const domain = [];

        if (this.state.selected_year !== "all") {
            domain.push(["year", "=", this.state.selected_year]);
        }

        // 🔹 STOCK (poultry.stock)
        const total_birds = await this.orm.searchCount("poultry.stock", domain);

        // 🔹 DEATH (poultry.death)
        const death_count = await this.orm.searchCount("poultry.death", domain);

        // 🔹 PURCHASE
        const purchase_total = await this.orm.searchRead(
            "poultry.purchase",
            domain,
            ["amount"]
        );

        // 🔹 SALE
        const sale_total = await this.orm.searchRead(
            "poultry.sale",
            domain,
            ["amount"]
        );

        // 🔹 CASH
        const cash_balance = await this.orm.searchRead(
            "poultry.cash",
            [],
            ["balance"]
        );

        const totalPurchase = purchase_total.reduce((s, r) => s + r.amount, 0);
        const totalSale = sale_total.reduce((s, r) => s + r.amount, 0);

        // UPDATE STATE
        this.state.total_birds = total_birds;
        this.state.death_count = death_count;

        this.state.purchase_total = totalPurchase;
        this.state.sale_total = totalSale;

        this.state.cash_balance = cash_balance[0]?.balance || 0;

        this.state.feed_stock = 1200; // replace with real model later

        this.state.mortality_rate =
            total_birds > 0 ? Math.round((death_count / total_birds) * 100) : 0;

        this.renderCharts();
    }

    // ================= YEAR FILTER =================
    async onYearChange(ev) {
        this.state.selected_year = ev.target.value;
        await this.loadData();
    }

    // ================= CHARTS =================
    renderCharts() {

        const deathCanvas = document.getElementById("deathChart");
        const profitCanvas = document.getElementById("profitChart");

        if (!deathCanvas || !profitCanvas) return;

        if (this.deathChart) this.deathChart.destroy();
        if (this.profitChart) this.profitChart.destroy();

        // DEATH CHART
        this.deathChart = new Chart(deathCanvas, {
            type: "line",
            data: {
                labels: ["Mon", "Tue", "Wed", "Thu", "Fri"],
                datasets: [{
                    label: "Deaths",
                    data: [2, 4, 1, 3, this.state.death_count],
                    borderWidth: 2
                }]
            }
        });

        // PROFIT CHART
        this.profitChart = new Chart(profitCanvas, {
            type: "bar",
            data: {
                labels: ["Purchase", "Sale"],
                datasets: [{
                    label: "Financial Flow",
                    data: [this.state.purchase_total, this.state.sale_total]
                }]
            }
        });
    }
}

PoultryDashboard.template = "poultry_dashboard.Main";

registry.category("actions").add("poultry_dashboard", PoultryDashboard);