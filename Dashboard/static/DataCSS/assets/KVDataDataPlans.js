document.addEventListener("DOMContentLoaded", function () {
    const networkInput = document.getElementById("network");      
    const dataTypeDiv = document.getElementById("dataType").parentElement;
    const dataTypeSelect = document.getElementById("dataType");
    const planSelect = document.getElementById("plan");
    const amountField = document.getElementById("amountField");
    const networkHeading = document.getElementById("networkName");

    // Plans per network & data type
    const plans = {
        MTN: {
            SME: [
                { plan_id: 7, type: "SME", amount: 700, size: "1.0 GB", validity: "30 days" },
                { plan_id: 8, type: "SME", amount: 1400, size: "2.0 GB", validity: "30 days" },
                { plan_id: 44, type: "SME", amount: 2100, size: "3.0 GB", validity: "30 days" },
                { plan_id: 214, type: "SME", amount: 8000, size: "10.0 GB", validity: "30 days" }
            ],
            GIFTING: [
                { plan_id: 384, type: "GIFTING", amount: 485, size: "1.0 GB", validity: "1 DAY" },
                { plan_id: 386, type: "GIFTING", amount: 970, size: "3.2 GB", validity: "2 DAYS" },
                { plan_id: 387, type: "GIFTING", amount: 2425, size: "6.0 GB", validity: "WEEKLY" },
                { plan_id: 396, type: "GIFTING", amount: 728, size: "2.0 GB", validity: "2 DAYS" },
                { plan_id: 398, type: "GIFTING", amount: 2910, size: "6.75 GB", validity: "30 DAYS (Xtra Special)" },
                { plan_id: 399, type: "GIFTING", amount: 4850, size: "14.5 GB", validity: "30 DAYS (Xtra Special)" },
                { plan_id: 400, type: "GIFTING", amount: 728, size: "1.2 GB", validity: "WEEKLY" },
                { plan_id: 401, type: "GIFTING", amount: 776, size: "1.0 GB", validity: "WEEKLY" },
                { plan_id: 402, type: "GIFTING", amount: 873, size: "2.5 GB", validity: "2 DAYS" },
                { plan_id: 403, type: "GIFTING", amount: 740, size: "2.5 GB", validity: "1 DAY" },
                { plan_id: 404, type: "GIFTING", amount: 970, size: "1.5 GB", validity: "WEEKLY" },
                { plan_id: 405, type: "GIFTING", amount: 1455, size: "2.0 GB", validity: "Monthly" },
                { plan_id: 406, type: "GIFTING", amount: 3395, size: "11.0 GB", validity: "WEEKLY" },
                { plan_id: 407, type: "GIFTING", amount: 5335, size: "12.5 GB", validity: "Monthly" },
                { plan_id: 408, type: "GIFTING", amount: 4365, size: "10.0 GB", validity: "Monthly" },
                { plan_id: 409, type: "GIFTING", amount: 6305, size: "16.5 GB", validity: "Monthly" },
                { plan_id: 411, type: "GIFTING", amount: 1455, size: "1.8 GB", validity: "N1500 airtime + 1.8GB (30days)" },
                { plan_id: 433, type: "GIFTING", amount: 5100, size: "20.0 GB", validity: "WEEKLY" },
                { plan_id: 436, type: "GIFTING", amount: 1455, size: "3.5 GB", validity: "WEEKLY" },
                { plan_id: 452, type: "GIFTING", amount: 3395, size: "7.0 GB", validity: "Monthly" },
                { plan_id: 458, type: "GIFTING", amount: 343, size: "500.0 MB", validity: "1 DAY" }
            ],
            "DATA COUPONS": [
                { plan_id: 442, type: "DATA COUPONS", amount: 540, size: "1.0 GB", validity: "Monthly" },
                { plan_id: 443, type: "DATA COUPONS", amount: 1000, size: "2.0 GB", validity: "Monthly" },
                { plan_id: 444, type: "DATA COUPONS", amount: 1500, size: "3.0 GB", validity: "Monthly" },
                { plan_id: 445, type: "DATA COUPONS", amount: 1800, size: "5.0 GB", validity: "Monthly" },
                { plan_id: 459, type: "DATA COUPONS", amount: 360, size: "500.0 MB", validity: "Monthly" },
                { plan_id: 460, type: "DATA COUPONS", amount: 450, size: "1.0 GB", validity: "Weekly" }
            ]
        },

        GLO: {
            "CORPORATE GIFTING": [
                { plan_id: 257, type: "CORPORATE GIFTING", amount: 200, size: "500.0 MB", validity: "Monthly" },
                { plan_id: 258, type: "CORPORATE GIFTING", amount: 390, size: "1.0 GB", validity: "Monthly" },
                { plan_id: 259, type: "CORPORATE GIFTING", amount: 780, size: "2.0 GB", validity: "Monthly" },
                { plan_id: 260, type: "CORPORATE GIFTING", amount: 1170, size: "3.0 GB", validity: "Monthly" },
                { plan_id: 261, type: "CORPORATE GIFTING", amount: 1950, size: "5.0 GB", validity: "Monthly" },
                { plan_id: 305, type: "CORPORATE GIFTING", amount: 3900, size: "10.0 GB", validity: "Monthly" },
                { plan_id: 332, type: "CORPORATE GIFTING", amount: 90, size: "200.0 MB", validity: "Monthly" }
            ],
            SME: [
                { plan_id: 357, type: "SME", amount: 195, size: "750.0 MB", validity: "DAILY" },
                { plan_id: 358, type: "SME", amount: 290, size: "1.5 GB", validity: "DAILY" },
                { plan_id: 359, type: "SME", amount: 480, size: "2.5 GB", validity: "2 DAYS" },
                { plan_id: 360, type: "SME", amount: 1900, size: "10.0 GB", validity: "WEEKLY" }
            ],
            GIFTING: [
                { plan_id: 461, type: "GIFTING", amount: 270, size: "1.0 GB", validity: "3 DAYS" },
                { plan_id: 462, type: "GIFTING", amount: 320, size: "1.0 GB", validity: "WEEKLY" },
                { plan_id: 463, type: "GIFTING", amount: 825, size: "3.0 GB", validity: "3 DAYS" },
                { plan_id: 464, type: "GIFTING", amount: 960, size: "3.0 GB", validity: "WEEKLY" },
                { plan_id: 465, type: "GIFTING", amount: 1380, size: "5.0 GB", validity: "3 DAYS" },
                { plan_id: 466, type: "GIFTING", amount: 1600, size: "5.0 GB", validity: "WEEKLY" }
            ]
        },

        AIRTEL: {
            GIFTING: [
                { plan_id: 412, type: "GIFTING", amount: 118, size: "100.0 MB", validity: "1 DAY" },
                { plan_id: 413, type: "GIFTING", amount: 196, size: "200.0 MB", validity: "2 DAYS" },
                { plan_id: 414, type: "GIFTING", amount: 294, size: "300.0 MB", validity: "2 DAYS" },
                { plan_id: 415, type: "GIFTING", amount: 490, size: "1.0 GB", validity: "1 DAY" },
                { plan_id: 416, type: "GIFTING", amount: 588, size: "1.5 GB", validity: "2 DAYS" },
                { plan_id: 417, type: "GIFTING", amount: 735, size: "2.0 GB", validity: "2 DAYS" },
                { plan_id: 418, type: "GIFTING", amount: 980, size: "3.0 GB", validity: "2 DAYS" },
                { plan_id: 419, type: "GIFTING", amount: 980, size: "1.5 GB", validity: "WEEKLY" },
                { plan_id: 420, type: "GIFTING", amount: 1470, size: "5.0 GB", validity: "2 DAYS" },
                { plan_id: 421, type: "GIFTING", amount: 1470, size: "2.0 GB", validity: "Monthly" },
                { plan_id: 422, type: "GIFTING", amount: 1470, size: "3.5 GB", validity: "WEEKLY" },
                { plan_id: 423, type: "GIFTING", amount: 1960, size: "3.0 GB", validity: "Monthly" },
                { plan_id: 424, type: "GIFTING", amount: 2450, size: "6.0 GB", validity: "WEEKLY" },
                { plan_id: 425, type: "GIFTING", amount: 2450, size: "4.0 GB", validity: "Monthly" },
                { plan_id: 426, type: "GIFTING", amount: 2940, size: "8.0 GB", validity: "Monthly" },
                { plan_id: 427, type: "GIFTING", amount: 3920, size: "10.0 GB", validity: "Monthly" },
                { plan_id: 428, type: "GIFTING", amount: 4900, size: "13.0 GB", validity: "Monthly" },
                { plan_id: 429, type: "GIFTING", amount: 4900, size: "18.0 GB", validity: "Monthly Router Plan" },
                { plan_id: 430, type: "GIFTING", amount: 5880, size: "18.0 GB", validity: "Monthly" },
                { plan_id: 431, type: "GIFTING", amount: 9800, size: "40.0 GB", validity: "Monthly (Router Plan)" },
                { plan_id: 437, type: "GIFTING", amount: 784, size: "1.0 GB", validity: "WEEKLY" },
                { plan_id: 449, type: "GIFTING", amount: 490, size: "500.0 MB", validity: "WEEKLY" },
                { plan_id: 457, type: "GIFTING", amount: 97000, size: "650.0 GB", validity: "365 days" }
            ],
            SME: [
                { plan_id: 391, type: "SME", amount: 345, size: "1.0 GB", validity: "2 DAYS" },
                { plan_id: 392, type: "SME", amount: 590, size: "2.0 GB", validity: "2 DAYS" },
                { plan_id: 393, type: "SME", amount: 980, size: "3.2 GB", validity: "2 DAYS" },
                { plan_id: 394, type: "SME", amount: 1970, size: "7.0 GB", validity: "WEEKLY" },
                { plan_id: 395, type: "SME", amount: 2950, size: "10.0 GB", validity: "Monthly" },
                { plan_id: 438, type: "SME", amount: 492, size: "1.5 GB", validity: "WEEKLY" },
                { plan_id: 439, type: "SME", amount: 396, size: "1.5 GB", validity: "1 DAY" },
                { plan_id: 440, type: "SME", amount: 1480, size: "5.0 GB", validity: "WEEKLY" },
                { plan_id: 441, type: "SME", amount: 740, size: "3.0 GB", validity: "2 DAYS" },
                { plan_id: 446, type: "SME", amount: 50, size: "150.0 MB", validity: "1 DAY" },
                { plan_id: 447, type: "SME", amount: 105, size: "300.0 MB", validity: "2 DAYS" },
                { plan_id: 448, type: "SME", amount: 200, size: "600.0 MB", validity: "2 DAYS" }
            ]
        },

        "9MOBILE": {
            "CORPORATE GIFTING": [
                { plan_id: 245, type: "CORPORATE GIFTING", amount: 140, size: "1.0 GB", validity: "Monthly" },
                { plan_id: 246, type: "CORPORATE GIFTING", amount: 280, size: "2.0 GB", validity: "Monthly" },
                { plan_id: 277, type: "CORPORATE GIFTING", amount: 420, size: "3.0 GB", validity: "Monthly" },
                { plan_id: 313, type: "CORPORATE GIFTING", amount: 85, size: "500.0 MB", validity: "Monthly" },
                { plan_id: 321, type: "CORPORATE GIFTING", amount: 700, size: "5.0 GB", validity: "Monthly" },
                { plan_id: 432, type: "CORPORATE GIFTING", amount: 3100, size: "10.0 GB", validity: "Monthly" }
            ]
        }
    };

    for (const network in plans) {
        for (const planType in plans[network]) {
            plans[network][planType].forEach(plan => {
                plan.amount += 20; // Add 20 Naira
            });
        }
    }

    // console.log(plans);

    // Handle network selection via circles
    document.querySelectorAll(".circle").forEach(circle => {
        circle.addEventListener("click", function () {
            const networkName = this.getAttribute("data-network").toUpperCase();

            // Update form
            networkInput.value = networkName;
            networkHeading.innerHTML = `${networkName} Data Bundles`;
            amountField.value = "";
            planSelect.innerHTML = '<option value="">---------</option>';

            // Highlight the clicked circle
            document.querySelectorAll(".circle").forEach(c => c.classList.remove("selected"));
            this.classList.add("selected");

            // Show form
            formContainer.style.display = "block";

            // Show/hide Data Type if MTN
            toggleDataType();
            loadPlans();
        });
    });

    // Show/Hide Data Type
    function toggleDataType() {
        if (networkInput.value === "MTN") {
            dataTypeDiv.style.display = "block";
        } else {
            dataTypeDiv.style.display = "none";
            dataTypeSelect.value = "";
        }
    }

    // Populate plan options
    function loadPlans() {
        planSelect.innerHTML = '<option value="">---------</option>';
        amountField.value = "";

        const net = networkInput.value;
        let availablePlans = [];

        if (net === "MTN") {
            const type = dataTypeSelect.value;
            availablePlans = plans.MTN[type] || [];
        } else {
            // merge all types for non-MTN
            const netPlans = plans[net];
            if (typeof netPlans === "object") {
                Object.values(netPlans).forEach(arr => availablePlans.push(...arr));
            } else {
                availablePlans = netPlans || [];
            }
        }

        availablePlans.forEach(plan => {
            const option = document.createElement("option");
            option.value = plan.plan_id;  // backend id
            option.textContent = `${plan.size} ${plan.type} = ₦${plan.amount} ${plan.validity}`;
            option.dataset.price = plan.amount;
            planSelect.appendChild(option);
        });
    }

    // Update amount field
    planSelect.addEventListener("change", function () {
        const selected = planSelect.options[planSelect.selectedIndex];
        amountField.value = selected.dataset.price || "";
    });

    dataTypeSelect.addEventListener("change", loadPlans);
});
