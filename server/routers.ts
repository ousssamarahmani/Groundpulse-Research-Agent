import { COOKIE_NAME } from "@shared/const";
import { z } from "zod";
import { getSessionCookieOptions } from "./_core/cookies";
import { systemRouter } from "./_core/systemRouter";
import { publicProcedure, router } from "./_core/trpc";

export const appRouter = router({
    // if you need to use socket.io, read and register route in server/_core/index.ts, all api should start with '/api/' so that the gateway can route correctly
  system: systemRouter,
  celestrak: router({
    latest: publicProcedure
      .input(z.object({ noradId: z.number().int().positive().default(25544) }))
      .query(async ({ input }) => {
        const sourceUrl = `https://celestrak.org/NORAD/elements/gp.php?CATNR=${input.noradId}&FORMAT=JSON`;
        const controller = new AbortController();
        const timeout = setTimeout(() => controller.abort(), 30_000);
        try {
          const response = await fetch(sourceUrl, {
            headers: { Accept: "application/json", "User-Agent": "GroundPulseResearchAgent/1.0" },
            signal: controller.signal,
          });
          if (!response.ok) throw new Error(`CelesTrak returned HTTP ${response.status}`);
          const rows = (await response.json()) as Array<Record<string, unknown>>;
          const row = rows[0];
          const meanMotion = Number(row?.MEAN_MOTION);
          if (!row || !Number.isFinite(meanMotion) || meanMotion <= 0) throw new Error("Invalid CelesTrak GP/OMM payload");
          return {
            source: "CelesTrak GP/OMM",
            sourceUrl,
            retrievedAt: new Date().toISOString(),
            objectName: String(row.OBJECT_NAME ?? "Unknown object"),
            objectId: String(row.OBJECT_ID ?? "Unknown object ID"),
            noradId: String(row.NORAD_CAT_ID ?? input.noradId),
            epoch: String(row.EPOCH ?? "Unknown epoch"),
            meanMotion,
            orbitalPeriodMinutes: 1440 / meanMotion,
          };
        } finally {
          clearTimeout(timeout);
        }
      }),
  }),
  auth: router({
    me: publicProcedure.query(opts => opts.ctx.user),
    logout: publicProcedure.mutation(({ ctx }) => {
      const cookieOptions = getSessionCookieOptions(ctx.req);
      ctx.res.clearCookie(COOKIE_NAME, { ...cookieOptions, maxAge: -1 });
      return {
        success: true,
      } as const;
    }),
  }),

  // TODO: add feature routers here, e.g.
  // todo: router({
  //   list: protectedProcedure.query(({ ctx }) =>
  //     db.getUserTodos(ctx.user.id)
  //   ),
  // }),
});

export type AppRouter = typeof appRouter;
