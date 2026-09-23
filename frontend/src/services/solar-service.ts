import { apiRequest } from "@/lib/api";
import type {
  SolarGenerationRecord,
  SolarSystem,
} from "@/types/solar";


export function getSolarSystem() {
  return apiRequest<SolarSystem>(
    "/solar/me/system"
  );
}


export function getSolarGeneration() {
  return apiRequest<SolarGenerationRecord[]>(
    "/solar/me/generation"
  );
}