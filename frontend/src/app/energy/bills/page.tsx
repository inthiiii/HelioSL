"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { FormEvent, useEffect, useState } from "react";

import { DashboardShell } from "@/components/layout/dashboard-shell";
import { isAuthenticated } from "@/lib/auth";
import {
  createConsumptionRecord,
  extractElectricityBill,
} from "@/services/energy-service";

import type { BillExtraction } from "@/types/energy";


export default function BillImportPage() {
  const router = useRouter();
  const [file, setFile] = useState<File | null>(null);
  const [extraction, setExtraction] =
    useState<BillExtraction | null>(null);
  const [billingMonth, setBillingMonth] = useState("");
  const [consumption, setConsumption] = useState("");
  const [billAmount, setBillAmount] = useState("");
  const [extracting, setExtracting] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");


  useEffect(() => {
    if (!isAuthenticated()) {
      router.replace("/login");
    }
  }, [router]);


  async function handleExtract(
    event: FormEvent<HTMLFormElement>
  ) {
    event.preventDefault();

    if (!file) {
      setError("Choose an electricity bill first.");
      return;
    }

    setExtracting(true);
    setError("");
    setSuccess("");

    try {
      const result = await extractElectricityBill(file);
      setExtraction(result);
      setBillingMonth(result.billing_month ?? "");
      setConsumption(result.consumption_kwh ?? "");
      setBillAmount(result.bill_amount_lkr ?? "");
    } catch (caught) {
      setExtraction(null);
      setError(
        caught instanceof Error
          ? caught.message
          : "Bill extraction failed."
      );
    } finally {
      setExtracting(false);
    }
  }


  async function handleSave(
    event: FormEvent<HTMLFormElement>
  ) {
    event.preventDefault();
    setError("");
    setSuccess("");

    const consumptionValue = Number(consumption);
    const amountValue = billAmount
      ? Number(billAmount)
      : null;

    if (!billingMonth || consumptionValue <= 0) {
      setError("Confirm a billing month and positive consumption value.");
      return;
    }

    setSaving(true);

    try {
      await createConsumptionRecord({
        billing_month: billingMonth,
        consumption_kwh: consumptionValue,
        bill_amount_lkr: amountValue,
      });
      setSuccess(
        "Consumption record saved. The original bill was not stored."
      );
    } catch (caught) {
      setError(
        caught instanceof Error
          ? caught.message
          : "Could not save this consumption record."
      );
    } finally {
      setSaving(false);
    }
  }


  return (
    <DashboardShell>
      <div className="mx-auto max-w-5xl">
        <p className="text-sm text-emerald-400">
          Private bill import
        </p>
        <h1 className="mt-2 text-3xl font-semibold text-white">
          Turn an electricity bill into energy data
        </h1>
        <p className="mt-3 max-w-3xl leading-7 text-neutral-400">
          Upload a text-based PDF, review the detected values, and
          choose what to save. HelioSL processes the bill in memory
          and does not keep the original document.
        </p>

        <div className="mt-8 grid gap-6 lg:grid-cols-[0.9fr_1.1fr]">
          <form
            onSubmit={handleExtract}
            className="rounded-2xl border border-neutral-800 bg-neutral-900 p-6"
          >
            <h2 className="text-xl font-semibold text-white">
              1. Upload and extract
            </h2>
            <p className="mt-2 text-sm leading-6 text-neutral-400">
              Accepted: text-based PDF, TXT or CSV, up to 5 MB. Scanned
              image-only bills require OCR and are not accepted yet.
            </p>

            <label className="mt-6 block rounded-2xl border border-dashed border-neutral-700 bg-neutral-950 p-6 text-center">
              <span className="block text-sm font-medium text-white">
                {file ? file.name : "Choose an electricity bill"}
              </span>
              <span className="mt-2 block text-xs text-neutral-500">
                Your document is never added to the knowledge base.
              </span>
              <input
                type="file"
                accept="application/pdf,text/plain,text/csv,.pdf,.txt,.csv"
                className="mt-4 block w-full text-sm text-neutral-400 file:mr-4 file:rounded-lg file:border-0 file:bg-emerald-400 file:px-4 file:py-2 file:font-medium file:text-neutral-950"
                onChange={(event) => {
                  setFile(event.target.files?.[0] ?? null);
                  setExtraction(null);
                  setError("");
                  setSuccess("");
                }}
              />
            </label>

            <button
              type="submit"
              disabled={!file || extracting}
              className="mt-5 w-full rounded-xl bg-emerald-400 px-5 py-3 font-semibold text-neutral-950 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {extracting ? "Reading bill..." : "Extract bill data"}
            </button>

            <div className="mt-6 rounded-xl border border-neutral-800 bg-neutral-950 p-4">
              <p className="text-sm font-medium text-white">
                Try a synthetic example
              </p>
              <div className="mt-3 flex flex-col gap-2 text-sm">
                <a
                  href="/samples/sample-ceb-household-bill.pdf"
                  download
                  className="text-emerald-400 hover:text-emerald-300"
                >
                  Download household CEB bill
                </a>
                <a
                  href="/samples/sample-leco-business-bill.pdf"
                  download
                  className="text-emerald-400 hover:text-emerald-300"
                >
                  Download business LECO bill
                </a>
              </div>
              <p className="mt-3 text-xs text-neutral-500">
                Samples are fictional and contain no customer data.
              </p>
            </div>
          </form>

          <div className="rounded-2xl border border-neutral-800 bg-neutral-900 p-6">
            <h2 className="text-xl font-semibold text-white">
              2. Review before saving
            </h2>

            {!extraction ? (
              <div className="mt-6 rounded-xl border border-neutral-800 bg-neutral-950 p-6 text-neutral-400">
                Extracted values will appear here. Nothing is saved
                until you confirm it.
              </div>
            ) : (
              <form onSubmit={handleSave} className="mt-6 space-y-5">
                <div className="grid gap-3 rounded-xl border border-neutral-800 bg-neutral-950 p-4 sm:grid-cols-2">
                  <Info label="Provider" value={extraction.provider ?? "Not detected"} />
                  <Info label="Account" value={extraction.account_number ?? "Not detected"} />
                  <Info
                    label="Confidence"
                    value={`${extraction.confidence} (${Math.round(extraction.confidence_score * 100)}%)`}
                  />
                  <Info label="File" value={extraction.filename} />
                </div>

                <Field
                  label="Billing month"
                  type="date"
                  value={billingMonth}
                  onChange={setBillingMonth}
                />
                <Field
                  label="Consumption (kWh)"
                  type="number"
                  value={consumption}
                  onChange={setConsumption}
                />
                <Field
                  label="Bill amount (LKR)"
                  type="number"
                  value={billAmount}
                  onChange={setBillAmount}
                  required={false}
                />

                {extraction.warnings.length > 0 && (
                  <div className="rounded-xl border border-amber-500/25 bg-amber-500/10 p-4">
                    <p className="text-sm font-medium text-amber-200">
                      Check these fields
                    </p>
                    <ul className="mt-2 space-y-1 text-sm text-amber-100/75">
                      {extraction.warnings.map((warning) => (
                        <li key={warning}>• {warning}</li>
                      ))}
                    </ul>
                  </div>
                )}

                <button
                  type="submit"
                  disabled={saving}
                  className="w-full rounded-xl bg-white px-5 py-3 font-semibold text-neutral-950 disabled:opacity-50"
                >
                  {saving ? "Saving..." : "Confirm and save record"}
                </button>
              </form>
            )}

            {error && (
              <p className="mt-5 rounded-xl border border-red-500/25 bg-red-500/10 p-4 text-sm text-red-200">
                {error}
              </p>
            )}
            {success && (
              <div className="mt-5 rounded-xl border border-emerald-500/25 bg-emerald-500/10 p-4 text-sm text-emerald-100">
                <p>{success}</p>
                <Link
                  href="/energy"
                  className="mt-2 inline-block font-semibold underline"
                >
                  View energy history
                </Link>
              </div>
            )}
          </div>
        </div>
      </div>
    </DashboardShell>
  );
}


function Info({
  label,
  value,
}: {
  label: string;
  value: string;
}) {
  return (
    <div>
      <p className="text-xs uppercase tracking-wide text-neutral-500">
        {label}
      </p>
      <p className="mt-1 break-words text-sm text-white">
        {value}
      </p>
    </div>
  );
}


function Field({
  label,
  type,
  value,
  onChange,
  required = true,
}: {
  label: string;
  type: "date" | "number";
  value: string;
  onChange: (value: string) => void;
  required?: boolean;
}) {
  return (
    <label className="block">
      <span className="text-sm text-neutral-300">
        {label}
      </span>
      <input
        type={type}
        value={value}
        required={required}
        min={type === "number" ? "0" : undefined}
        step={type === "number" ? "0.01" : undefined}
        onChange={(event) => onChange(event.target.value)}
        className="mt-2 w-full rounded-xl border border-neutral-700 bg-neutral-950 px-4 py-3 text-white outline-none focus:border-emerald-400"
      />
    </label>
  );
}
