export interface SidenavItem {
  label: string;
  icon: string;
  route?: string;
  action?: () => void;
}
